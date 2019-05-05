from powerbiclient.server import RequestFactory

from .endpoint import Endpoint, api
import logging

logger = logging.getLogger('powerbi.endpoint.auth')


class Auth(Endpoint):
    class contextmgr(object):
        def __init__(self, callback):
            self._callback = callback

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._callback()

    @property
    def baseurl(self):
        return "{0}".format(self.parent_srv.authurl)

    @api(version="1.0")
    def acquire_token(self, auth_req):
        url = "{0}".format(self.parent_srv.authurl)
        signin_req = RequestFactory.Auth.signin_req(auth_req)
        server_response = self.parent_srv.session.post(url, data=signin_req, **self.parent_srv.http_options)
        self._check_status(server_response)
        auth_token = server_response.json()['access_token']
        self.parent_srv._set_auth(auth_req.username, auth_token)
        logger.info('got token from {0} for {1}'.format(self.parent_srv.authurl, auth_req.username))
        return Auth.contextmgr(self.release_token)

    @api(version="1.0")
    def release_token(self):
        # If there are no auth tokens you're already signed out. No-op
        if not self.parent_srv.is_signed_in():
            return
        self.parent_srv.clear_auth()
        logger.info('signed out')
        # no-op for Power BI
