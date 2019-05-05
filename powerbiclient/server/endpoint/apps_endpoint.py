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

    # get dashboards
    @api(version="1.0")
    def get_dashboards(self, app):
        if not app or not app.id:
            error = "app ID undefined"
            raise ValueError(error)
        logger.info('querying dashboards for app (ID: {0})'.format(app.id))
        url = "{0}/{1}/dashboards".format(self.baseurl, app.id)
        server_response = self.get_request(url)
        return DashboardItem.from_response(server_response)

    # get dashboard by id
    @api(version="1.0")
    def get_dashboard_by_id(self, app, dashboard_id):
        if not app or not app.id:
            error = "app ID undefined"
            raise ValueError(error)
        logger.info('querying single dashboard (ID: {0}, app ID: {1})'.format(dashboard_id, app.id))
        url = "{0}/{1}/dashboards/{2}".format(self.baseurl, app.id, dashboard_id)
        server_response = self.get_request(url)
        return DashboardItem.from_response(server_response)

    # get reports
    @api(version="1.0")
    def get_reports(self, app):
        if not app or not app.id:
            error = "app ID undefined"
            raise ValueError(error)
        logger.info('querying reports for app (ID: {0})'.format(app.id))
        url = "{0}/{1}/reports".format(self.baseurl, app.id)
        server_response = self.get_request(url)
        return ReportItem.from_response(server_response)

    # get report by id
    @api(version="1.0")
    def get_report_by_id(self, app, report_id):
        if not app or not app.id:
            error = "app ID undefined"
            raise ValueError(error)
        logger.info('querying single report (ID: {0}, app ID: {1})'.format(report_id, app.id))
        url = "{0}/{1}/reports/{2}".format(self.baseurl, app.id, report_id)
        server_response = self.get_request(url)
        return ReportItem.from_response(server_response)

    # get tiles
    @api(version="1.0")
    def get_tiles(self, app):
        if not app or not app.id:
            error = "app ID undefined"
            raise ValueError(error)
        logger.info('querying tiles for app (ID: {0})'.format(app.id))
        url = "{0}/{1}/tiles".format(self.baseurl, app.id)
        server_response = self.get_request(url)
        return TileItem.from_response(server_response)

    # get tile by id
    @api(version="1.0")
    def get_tile_by_id(self, app, tile_id):
        if not app or not app.id:
            error = "app ID undefined"
            raise ValueError(error)
        logger.info('querying single tile (ID: {0}, app ID: {1})'.format(tile_id, app.id))
        url = "{0}/{1}/tiles/{2}".format(self.baseurl, app.id, tile_id)
        server_response = self.get_request(url)
        return TileItem.from_response(server_response)
