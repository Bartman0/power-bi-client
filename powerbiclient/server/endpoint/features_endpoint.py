import logging

from .endpoint import api, Endpoint
from .. import FeatureItem

logger = logging.getLogger('powerbi.endpoint.features')


class Features(Endpoint):
    def __init__(self, parent_srv):
        super(Features, self).__init__(parent_srv)

    @property
    def baseurl(self):
        return "{0}/availableFeatures".format(self.parent_srv.baseurl)

    # get all features
    @api(version="1.0")
    def get(self, req_options=None):
        logger.info('querying all features')
        url = self.baseurl
        server_response = self.get_request(url, req_options)
        all_feature_items = FeatureItem.from_response(server_response)
        return all_feature_items

    # get 1 feature by name
    @api(version="1.0")
    def get_by_name(self, feature_name):
        if not feature_name:
            error = "feature name undefined"
            raise ValueError(error)
        logger.info('querying single feature (name: {0})'.format(feature_name))
        url = "{0}(featureName='{1}')".format(self.baseurl, feature_name)
        server_response = self.get_request(url)
        return FeatureItem.from_response(server_response)[0]
