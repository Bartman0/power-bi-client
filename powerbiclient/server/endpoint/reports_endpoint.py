import logging

from ..request_factory import RequestFactory
from .endpoint import api, Endpoint
from .. import ReportItem

logger = logging.getLogger('powerbi.endpoint.reports')


class Reports(Endpoint):
    def __init__(self, parent_srv):
        super(Reports, self).__init__(parent_srv)

    @property
    def baseurl(self):
        return "{0}/reports".format(self.parent_srv.baseurl)

    # get all reports
    @api(version="1.0")
    def get(self, req_options=None):
        logger.info('querying reports')
        url = self.baseurl
        server_response = self.get_request(url, req_options)
        all_report_items = ReportItem.from_response(server_response)
        return all_report_items

    # get 1 report by id
    @api(version="1.0")
    def get_by_id(self, report_id):
        if not report_id:
            error = "report ID undefined"
            raise ValueError(error)
        logger.info('querying single report (ID: {0})'.format(report_id))
        url = "{0}/{1}".format(self.baseurl, report_id)
        server_response = self.get_request(url)
        return ReportItem.from_response(server_response)[0]

    # delete 1 report by id
    @api(version="1.0")
    def delete(self, report_id):
        if not report_id:
            error = "report ID undefined"
            raise ValueError(error)
        url = "{0}/{1}".format(self.baseurl, report_id)
        self.delete_request(url)
        logger.info('deleted single report (ID: {0})'.format(report_id))

    # clone 1 report by id
    @api(version="1.0")
    def clone(self, report_id, name, target_model_id=None, target_workspace_id=None):
        if not report_id:
            error = "report ID undefined"
            raise ValueError(error)
        url = "{0}/{1}/Clone".format(self.baseurl, report_id)
        post_req = RequestFactory.Report.clone(name, target_model_id, target_workspace_id)
        server_response = self.post_request(url, post_req)
        logger.info('cloned single report (ID: {0})'.format(report_id))
        all_report_items = ReportItem.from_response(server_response)
        return all_report_items

    # export 1 report by id
    @api(version="1.0")
    def export(self, report_id):
        if not report_id:
            error = "report ID undefined"
            raise ValueError(error)
        url = "{0}/{1}/Export".format(self.baseurl, report_id)
        server_response = self.get_request(url)
        logger.info('exported single report (ID: {0})'.format(report_id))
        return server_response      # expect application/zip data contents
