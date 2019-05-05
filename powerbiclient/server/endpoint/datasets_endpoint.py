import logging

from .endpoint import api, Endpoint
from .. import RequestFactory, DatasetItem, TableItem

logger = logging.getLogger('powerbi.endpoint.datasets')


class Datasets(Endpoint):
    def __init__(self, parent_srv):
        super(Datasets, self).__init__(parent_srv)

    @property
    def baseurl(self):
        return "{0}/datasets".format(self.parent_srv.baseurl)

    # get all datasets
    @api(version="1.0")
    def get(self, req_options=None):
        logger.info('querying all datasets')
        url = self.baseurl
        server_response = self.get_request(url, req_options)
        all_dataset_items = DatasetItem.from_response(server_response)
        return all_dataset_items

    # get 1 dataset by id
    @api(version="1.0")
    def get_by_id(self, dataset_id):
        if not dataset_id:
            error = "dataset ID undefined"
            raise ValueError(error)
        logger.info('querying single dataset (ID: {0})'.format(dataset_id))
        url = "{0}/{1}".format(self.baseurl, dataset_id)
        server_response = self.get_request(url)
        return DatasetItem.from_response(server_response)[0]

    # delete 1 dataset by id
    @api(version="1.0")
    def delete(self, dataset_id):
        if not dataset_id:
            error = "dataset ID undefined"
            raise ValueError(error)
        url = "{0}/{1}".format(self.baseurl, dataset_id)
        self.delete_request(url)
        logger.info('deleted single dataset (ID: {0})'.format(dataset_id))

    # push dataset
    @api(version="1.0")
    def post_dataset(self, name, tables, default_retention_policy="None"):
        url = "{0}?defaultRetentionPolicy={1}".format(self.baseurl, default_retention_policy)
        push_req = RequestFactory.Dataset.post_dataset(name, tables)
        server_response = self.post_request(url, push_req)
        dataset_item = DatasetItem.from_response(server_response)
        logger.info('pushed dataset item (ID: {0})'.format(dataset_item[0].id))
        return dataset_item[0]

    # refresh dataset
    def refresh(self, dataset_item):
        url = "{0}/{1}/refreshes".format(self.baseurl, dataset_item.id)
        req = RequestFactory.Dataset.refresh('MailOnFailure')
        server_response = self.post_request(url, req)
        return server_response

    # get all tables
    @api(version="1.0")
    def get_tables(self, dataset, req_options=None):
        logger.info('querying all tables in dataset')
        url = "{0}/{1}/tables".format(self.baseurl, dataset.id)
        server_response = self.get_request(url, req_options)
        all_table_items = TableItem.from_response(dataset, server_response)
        return all_table_items

    # post rows to a table
    @api(version="1.0")
    def post_rows(self, dataset, table_name, rows):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        if not table_name:
            error = "table name undefined"
            raise ValueError(error)
        logger.info('post rows to table (name: {0}) for dataset (ID: {1})'.format(table_name, dataset.id))
        url = "{0}/{1}/tables/{2}/rows".format(self.baseurl, dataset.id, table_name)
        post_req = RequestFactory.Dataset.post_rows(rows)
        self.post_request(url, post_req)
