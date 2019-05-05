from .endpoint import Auth, Capacities, Datasets, Tables, Apps, ServerInfo

import requests


class Server(object):
    def __init__(self):
        self._auth_address = "https://login.microsoftonline.com/common/oauth2/token"
        self._auth_token = None
        self._user_id = None
        self._session = requests.Session()
        self._http_options = dict()

        self.auth = Auth(self)
        self.capacities = Capacities(self)
        self.datasets = Datasets(self)
        self.apps = Apps(self)
        self.tables = Tables(self)
        self.server_info = ServerInfo(self).get()
        self.version = self.server_info.rest_api_version    # the server version is equal to the API version
        self._server_address = "https://api.powerbi.com/v{0}/myorg".format(str(self.version))

    def add_http_options(self, options_dict):
        self._http_options.update(options_dict)

    def clear_http_options(self):
        self._http_options = dict()

    def clear_auth(self):
        self._user_id = None
        self._auth_token = None
        self._session = requests.Session()

    def _set_auth(self, user_id, auth_token):
        self._user_id = user_id
        self._auth_token = auth_token

    @property
    def baseurl(self):
        return "{0}".format(self._server_address)

    @property
    def authurl(self):
        return "{0}".format(self._auth_address)

    @property
    def auth_token(self):
        if self._auth_token is None:
            error = 'missing authentication token, you must sign in first'
            raise NotSignedInError(error)
        return self._auth_token

    @property
    def user_id(self):
        if self._user_id is None:
            error = 'missing user ID, you must sign in first'
            raise NotSignedInError(error)
        return self._user_id

    @property
    def server_address(self):
        return self._server_address

    @property
    def auth_address(self):
        return self._auth_address

    @property
    def http_options(self):
        return self._http_options

    @property
    def session(self):
        return self._session

    def is_signed_in(self):
        return self._auth_token is not None
