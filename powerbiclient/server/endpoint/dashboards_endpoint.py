import logging

from .endpoint import api, Endpoint
from .. import DashboardItem, TileItem

logger = logging.getLogger('powerbi.endpoint.dashboards')


class Dashboards(Endpoint):
    def __init__(self, parent_srv):
        super(Dashboards, self).__init__(parent_srv)

    @property
    def baseurl(self):
        return "{0}/dashboards".format(self.parent_srv.baseurl)

    # get all dashboards
    @api(version="1.0")
    def get(self, req_options=None):
        logger.info('querying dashboards')
        url = self.baseurl
        server_response = self.get_request(url, req_options)
        all_dashboard_items = DashboardItem.from_response(server_response)
        return all_dashboard_items

    # get 1 dashboard by id
    @api(version="1.0")
    def get_by_id(self, dashboard_id):
        if not dashboard_id:
            error = "dashboard ID undefined"
            raise ValueError(error)
        logger.info('querying single dashboard (ID: {0})'.format(dashboard_id))
        url = "{0}/dashboards/{1}".format(self.baseurl, dashboard_id)
        server_response = self.get_request(url)
        return DashboardItem.from_response(server_response)[0]

    # get tiles
    @api(version="1.0")
    def get_tiles(self, dashboard):
        if not dashboard or not dashboard.id:
            error = "dashboard ID undefined"
            raise ValueError(error)
        logger.info('querying tiles for dashboard (ID: {0})'.format(dashboard.id))
        url = "{0}/{1}/tiles".format(self.baseurl, dashboard.id)
        server_response = self.get_request(url)
        return TileItem.from_response(server_response)

    # get tile by id
    @api(version="1.0")
    def get_tile_by_id(self, dashboard, tile_id):
        if not dashboard or not dashboard.id:
            error = "dashboard ID undefined"
            raise ValueError(error)
        if not tile_id:
            error = "tile ID undefined"
            raise ValueError(error)
        logger.info('querying single tile (ID: {0} for dashboard (ID: {1})'.format(tile_id, dashboard.id))
        url = "{0}/{1}/tiles/{2}".format(self.baseurl, dashboard.id, tile_id)
        server_response = self.get_request(url)
        return TileItem.from_response(server_response)
