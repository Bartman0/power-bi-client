class ServerInfoItem(object):
    def __init__(self, rest_api_version):
        self._rest_api_version = rest_api_version

    @property
    def rest_api_version(self):
        return self._rest_api_version
