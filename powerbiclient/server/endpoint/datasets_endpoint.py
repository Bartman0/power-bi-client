import logging

from .endpoint import api, Endpoint
from .. import RequestFactory, DatasetItem, TableItem, DatasourceItem, ParameterItem, ScheduleItem

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

    # get dataset by name
    @api(version="1.0")
    def get_by_name(self, name, req_options=None):
        logger.info('querying all datasets')
        url = self.baseurl
        server_response = self.get_request(url, req_options)
        all_dataset_items = DatasetItem.from_response(server_response)
        for item in all_dataset_items:
            if item.name == name:
                return item
        return None

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
        if not name:
            error = "name undefined"
            raise ValueError(error)
        if not tables:
            error = "tables not set"
            raise ValueError(error)
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

    # get all datasources
    @api(version="1.0")
    def get_datasources(self, dataset, req_options=None):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        logger.info('querying all datasources in dataset')
        url = "{0}/{1}/datasources".format(self.baseurl, dataset.id)
        server_response = self.get_request(url, req_options)
        all_datasource_items = DatasourceItem.from_response(server_response, dataset)
        return all_datasource_items

    # get all parameters
    @api(version="1.0")
    def get_parameters(self, dataset, req_options=None):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        logger.info('querying all parameters in dataset')
        url = "{0}/{1}/parameters".format(self.baseurl, dataset.id)
        server_response = self.get_request(url, req_options)
        all_parameter_items = ParameterItem.from_response(server_response, dataset)
        return all_parameter_items

    # get all schedules
    @api(version="1.0")
    def get_schedules(self, dataset, req_options=None):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        logger.info('querying all schedules in dataset')
        url = "{0}/{1}/refreshSchedule".format(self.baseurl, dataset.id)
        server_response = self.get_request(url, req_options)
        all_schedule_items = ScheduleItem.from_response(server_response, dataset)
        return all_schedule_items

    # get all tables
    @api(version="1.0")
    def get_tables(self, dataset, req_options=None):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        logger.info('querying all tables in dataset')
        url = "{0}/{1}/tables".format(self.baseurl, dataset.id)
        server_response = self.get_request(url, req_options)
        all_table_items = TableItem.from_response(server_response, dataset)
        return all_table_items

    # get table by name
    @api(version="1.0")
    def get_table_by_name(self, dataset, name, req_options=None):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        logger.info('querying all tables in dataset')
        url = "{0}/{1}/tables".format(self.baseurl, dataset.id)
        server_response = self.get_request(url, req_options)
        all_table_items = TableItem.from_response(server_response, dataset)
        for item in all_table_items:
            if item.name == name:
                return item
        return None

    # post rows to a table
    @api(version="1.0")
    def post_rows(self, dataset, table_name, rows):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        if not table_name:
            error = "table name undefined"
            raise ValueError(error)
        if not rows:
            error = "rows undefined"
            raise ValueError(error)
        logger.info('post rows to table (name: {0}) for dataset (ID: {1})'.format(table_name, dataset.id))
        url = "{0}/{1}/tables/{2}/rows".format(self.baseurl, dataset.id, table_name)
        post_req = RequestFactory.Dataset.post_rows(rows)
        self.post_request(url, post_req)

    # delete rows from a table
    @api(version="1.0")
    def delete_rows(self, dataset, table_name):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        if not table_name:
            error = "table name undefined"
            raise ValueError(error)
        url = "{0}/{1}/tables/{2}/rows".format(self.baseurl, dataset.id, table_name)
        self.delete_request(url)
        logger.info('deleted rows from table (name: {0}) for dataset (ID: {1})'.format(table_name, dataset.id))

    # post rows to a table
    @api(version="1.0")
    def put_table(self, dataset, table_name, schema):
        if not dataset or not dataset.id:
            error = "dataset ID undefined"
            raise ValueError(error)
        if not table_name:
            error = "table name undefined"
            raise ValueError(error)
        if not schema:
            error = "schema undefined"
            raise ValueError(error)
        logger.info('put schema to table (name: {0}) for dataset (ID: {1})'.format(table_name, dataset.id))
        url = "{0}/{1}/tables/{2}".format(self.baseurl, dataset.id, table_name)
        put_req = RequestFactory.Dataset.put_table(schema)
        self.put_request(url, put_req)
