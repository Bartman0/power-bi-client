from .. import RequestFactory, DatasetItem
from .endpoint import api, parameter_added_in, Endpoint
from .exceptions import MissingRequiredFieldError
import os
import logging
import copy
import cgi
from contextlib import closing

logger = logging.getLogger('powerbi.endpoint.datasets')


class Datasets(Endpoint):
    def __init__(self, parent_srv):
        super(Datasets, self).__init__(parent_srv)

    @property
    def baseurl(self):
        return "{0}/datasets".format(self.parent_srv.baseurl)

    # Get all datasets
    @api(version="1.0")
    def get(self, req_options=None):
        logger.info('querying all datasets')
        url = self.baseurl
        server_response = self.get_request(url, req_options)
        all_dataset_items = DatasetItem.from_response(server_response)
        return all_dataset_items

    # Get 1 dataset by id
    @api(version="1.0")
    def get_by_id(self, dataset_id):
        if not dataset_id:
            error = "dataset ID undefined"
            raise ValueError(error)
        logger.info('querying single dataset (ID: {0})'.format(dataset_id))
        url = "{0}/{1}".format(self.baseurl, dataset_id)
        server_response = self.get_request(url)
        return DatasetItem.from_response(server_response)[0]

    # Delete 1 dataset by id
    @api(version="1.0")
    def delete(self, dataset_id):
        if not dataset_id:
            error = "dataset ID undefined"
            raise ValueError(error)
        url = "{0}/{1}".format(self.baseurl, dataset_id)
        self.delete_request(url)
        logger.info('deleted single dataset (ID: {0})'.format(dataset_id))

    # Download 1 dataset by id
    @api(version="1.0")
    @parameter_added_in(no_extract='2.5')
    @parameter_added_in(include_extract='2.5')
    def download(self, dataset_id, filepath=None, include_extract=True, no_extract=None):
        if not dataset_id:
            error = "Datasource ID undefined."
            raise ValueError(error)
        url = "{0}/{1}/content".format(self.baseurl, dataset_id)

        if no_extract is False or no_extract is True:
            import warnings
            warnings.warn('no_extract is deprecated, use include_extract instead.', DeprecationWarning)
            include_extract = not no_extract

        if not include_extract:
            url += "?includeExtract=False"

        with closing(self.get_request(url, parameters={'stream': True})) as server_response:
            _, params = cgi.parse_header(server_response.headers['Content-Disposition'])
            filename = to_filename(os.path.basename(params['filename']))
            if filepath is None:
                filepath = filename
            elif os.path.isdir(filepath):
                filepath = os.path.join(filepath, filename)

            with open(filepath, 'wb') as f:
                for chunk in server_response.iter_content(1024):  # 1KB
                    f.write(chunk)

        logger.info('Downloaded dataset to {0} (ID: {1})'.format(filepath, dataset_id))
        return os.path.abspath(filepath)

    # push dataset
    @api(version="1.0")
    def post_dataset(self, name, tables, defaultRetentionPolicy="None"):
        url = "{0}?defaultRetentionPolicy={1}".format(self.baseurl, defaultRetentionPolicy)
        push_req = RequestFactory.Dataset.post_dataset(name, tables)
        server_response = self.post_request(url, push_req)
        dataset_item = DatasetItem.from_response(server_response)
        logger.info('pushed dataset item (ID: {0})'.format(dataset_item[0].id))
        return dataset_item[0]

    def refresh(self, dataset_item):
        url = "{0}/{1}/refreshes".format(self.baseurl, dataset_item.id)
        req = RequestFactory.Dataset.refresh('MailOnFailure')
        server_response = self.post_request(url, req)
        return server_response
