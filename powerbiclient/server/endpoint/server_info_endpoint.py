from .endpoint import Endpoint
from powerbiclient.models import ServerInfoItem
import logging

logger = logging.getLogger('powerbi.endpoint.server_info')

API_VERSION = "1.0"     # hard coded


class ServerInfo(Endpoint):
    @property
    def baseurl(self):
        # no server call in Power BI yet
        return "{0}/null".format(self.parent_srv.baseurl)

    def get(self):
        server_info = ServerInfoItem(API_VERSION)
        return server_info
