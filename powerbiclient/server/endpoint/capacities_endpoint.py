import logging

from powerbiclient.server import RequestFactory
from .endpoint import api, Endpoint
from .. import CapacityItem, WorkloadItem

logger = logging.getLogger('powerbi.endpoint.capacities')


class Capacities(Endpoint):
    def __init__(self, parent_srv):
        super(Capacities, self).__init__(parent_srv)

    @property
    def baseurl(self):
        return "{0}/capacities".format(self.parent_srv.baseurl)

    # get all capacities
    @api(version="1.0")
    def get(self, req_options=None):
        logger.info('querying capacities')
        url = self.baseurl
        server_response = self.get_request(url, req_options)
        all_capacity_items = CapacityItem.from_response(server_response)
        return all_capacity_items

    # get workloads
    @api(version="1.0")
    def get_workloads(self, capacity):
        if not capacity or not capacity.id:
            error = "capacity ID undefined"
            raise ValueError(error)
        logger.info('querying workloads for capacity (ID: {0})'.format(capacity.id))
        url = "{0}/{1}/Workloads".format(self.baseurl, capacity.id)
        server_response = self.get_request(url)
        return WorkloadItem.from_response(server_response)

    # get 1 workload by name
    @api(version="1.0")
    def get_by_name(self, capacity, workload_name):
        if not capacity or not capacity.id:
            error = "capacity ID undefined"
            raise ValueError(error)
        if not workload_name:
            error = "workload name undefined"
            raise ValueError(error)
        logger.info('querying single workload (name: {0}) for capacity (ID: {1})'.format(workload_name, capacity.id))
        url = "{0}/{1}/Workloads/{2}".format(self.baseurl, capacity.id, workload_name)
        server_response = self.get_request(url)
        return WorkloadItem.from_response(server_response)[0]

    # patch 1 workload by name
    @api(version="1.0")
    def patch_workload(self, capacity, workload_name, state, maxMemoryPercentageSetByUser):
        if not capacity or not capacity.id:
            error = "capacity ID undefined"
            raise ValueError(error)
        if not workload_name:
            error = "workload name undefined"
            raise ValueError(error)
        logger.info('patching single workload (name: {0}) for capacity (ID: {1})'.format(workload_name, capacity.id))
        url = "{0}/{1}/Workloads/{2}".format(self.baseurl, capacity.id, workload_name)
        req = RequestFactory.Capacity.patch_workload(state, maxMemoryPercentageSetByUser)
        server_response = self.get_request(url, )
        return WorkloadItem.from_response(server_response)[0]
