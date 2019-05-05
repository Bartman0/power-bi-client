from .. import RequestFactory, DatasetItem, CapacityItem
from .endpoint import api, parameter_added_in, Endpoint
from .exceptions import MissingRequiredFieldError
import os
import logging
import copy
import cgi
from contextlib import closing

logger = logging.getLogger('powerbi.endpoint.capacities')


class Capacities(Endpoint):
    def __init__(self, parent_srv):
        super(Capacities, self).__init__(parent_srv)

    @property
    def baseurl(self):
        return "{0}/capacities".format(self.parent_srv.baseurl)

    # Get all capacities
    @api(version="1.0")
    def get(self, req_options=None):
        logger.info('querying capacities')
        url = self.baseurl
        server_response = self.get_request(url, req_options)
        all_capacity_items = CapacityItem.from_response(server_response)
        return all_capacity_items
