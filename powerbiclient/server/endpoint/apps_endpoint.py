from .endpoint import api, Endpoint
from .. import AppItem

import logging

logger = logging.getLogger('powerbi.endpoint.apps')


class Apps(Endpoint):
    def __init__(self, parent_srv):
        super(Apps, self).__init__(parent_srv)

    @property
    def baseurl(self):
        return "{0}/apps".format(self.parent_srv.baseurl)

    # get all apps
    @api(version="1.0")
    def get(self, req_options=None):
        logger.info('querying all apps')
        url = self.baseurl
        server_response = self.get_request(url, req_options)
        all_app_items = AppItem.from_response(server_response)
        return all_app_items

    # get 1 app
    @api(version="1.0")
    def get_by_id(self, app_id):
        if not app_id:
            error = "app ID undefined"
            raise ValueError(error)
        logger.info('querying single app (ID: {0})'.format(app_id))
        url = "{0}/{1}".format(self.baseurl, app_id)
        server_response = self.get_request(url)
        return AppItem.from_response(server_response)
