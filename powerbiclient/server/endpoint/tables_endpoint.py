from .endpoint import api, parameter_added_in, Endpoint
from .exceptions import MissingRequiredFieldError
from .. import RequestFactory, TableItem

import os
import logging
import copy

logger = logging.getLogger('powerbi.endpoint.tables')


class Tables(Endpoint):
    def __init__(self, parent_srv):
        super(Tables, self).__init__(parent_srv)

    def baseurl(self, dataset_id):
        return "{0}/datasets/{1}/tables".format(self.parent_srv.baseurl, dataset_id)

    # get all tables
    @api(version="1.0")
    def get(self, dataset, req_options=None):
        logger.info('querying all tables in dataset')
        url = self.baseurl(dataset.id)
        server_response = self.get_request(url, req_options)
        all_table_items = TableItem.from_response(dataset, server_response)
        return all_table_items

    # get 1 table
    @api(version="1.0")
    def get_by_id(self, dataset, table_name):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        if not table_name:
            error = "table name undefined"
            raise ValueError(error)
        logger.info('querying single table (name: {0})'.format(table_name))
        url = "{0}/{1}".format(self.baseurl(dataset.id), table_name)
        server_response = self.get_request(url)
        return TableItem.from_response(server_response)[0]

    # get 1 table
    @api(version="1.0")
    def post_rows(self, dataset, table, rows):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        if not table or not table.name:
            error = "table name undefined"
            raise ValueError(error)
        logger.info('post rows to table (name: {0})'.format(table.name))
        url = "{0}/{1}/rows".format(self.baseurl(dataset.id), table.name)
        post_req = RequestFactory.Dataset.post_rows(rows)
        self.post_request(url, post_req)

    # Update workbook
    @api(version="2.0")
    def update(self, workbook_item):
        if not workbook_item.id:
            error = "Workbook item missing ID. Workbook must be retrieved from server first."
            raise MissingRequiredFieldError(error)

        self._resource_tagger.update_tags(self.baseurl, workbook_item)

        # Update the workbook itself
        url = "{0}/{1}".format(self.baseurl, workbook_item.id)
        update_req = RequestFactory.Workbook.update_req(workbook_item)
        server_response = self.put_request(url, update_req)
        logger.info('Updated workbook item (ID: {0}'.format(workbook_item.id))
        updated_workbook = copy.copy(workbook_item)
        return updated_workbook._parse_common_tags(server_response.content, self.parent_srv.namespace)

    # Publishes workbook. Chunking method if file over 64MB
    @api(version="2.0")
    @parameter_added_in(connections='2.8')
    def publish(self, workbook_item, file_path, mode, connection_credentials=None, connections=None):

        if connection_credentials is not None:
            import warnings
            warnings.warn("connection_credentials is being deprecated. Use connections instead",
                          DeprecationWarning)

        if not os.path.isfile(file_path):
            error = "File path does not lead to an existing file."
            raise IOError(error)
        if not hasattr(self.parent_srv.PublishMode, mode):
            error = 'Invalid mode defined.'
            raise ValueError(error)

        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(filename)[1][1:]

        # If name is not defined, grab the name from the file to publish
        if not workbook_item.name:
            workbook_item.name = os.path.splitext(filename)[0]
        if file_extension not in ALLOWED_FILE_EXTENSIONS:
            error = "Only {} files can be published as workbooks.".format(', '.join(ALLOWED_FILE_EXTENSIONS))
            raise ValueError(error)

        # Construct the url with the defined mode
        url = "{0}?workbookType={1}".format(self.baseurl, file_extension)
        if mode == self.parent_srv.PublishMode.Overwrite:
            url += '&{0}=true'.format(mode.lower())
        elif mode == self.parent_srv.PublishMode.Append:
            error = 'Workbooks cannot be appended.'
            raise ValueError(error)

        # Determine if chunking is required (64MB is the limit for single upload method)
        if os.path.getsize(file_path) >= FILESIZE_LIMIT:
            logger.info('Publishing {0} to server with chunking method (workbook over 64MB)'.format(filename))
            upload_session_id = Fileuploads.upload_chunks(self.parent_srv, file_path)
            url = "{0}&uploadSessionId={1}".format(url, upload_session_id)
            conn_creds = connection_credentials
            xml_request, content_type = RequestFactory.Workbook.publish_req_chunked(workbook_item,
                                                                                    connection_credentials=conn_creds,
                                                                                    connections=connections)
        else:
            logger.info('Publishing {0} to server'.format(filename))
            with open(file_path, 'rb') as f:
                file_contents = f.read()
            conn_creds = connection_credentials
            xml_request, content_type = RequestFactory.Workbook.publish_req(workbook_item,
                                                                            filename,
                                                                            file_contents,
                                                                            connection_credentials=conn_creds,
                                                                            connections=connections)
        logger.debug('Request xml: {0} '.format(xml_request[:1000]))
        server_response = self.post_request(url, xml_request, content_type)
        new_workbook = WorkbookItem.from_response(server_response.content, self.parent_srv.namespace)[0]
        logger.info('Published {0} (ID: {1})'.format(filename, new_workbook.id))
        return new_workbook
