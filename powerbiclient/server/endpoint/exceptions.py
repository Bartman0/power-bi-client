import json

class ServerResponseError(Exception):
    def __init__(self, code, summary, detail):
        self.code = code
        self.summary = summary
        self.detail = detail
        super(ServerResponseError, self).__init__(str(self))

    def __str__(self):
        return "response code {0}: {1}, {2}".format(self.code, self.summary, self.detail)

    @classmethod
    def from_response(cls, resp):
        if len(resp.content) > 0:
            error = json.loads(resp.content.decode('utf-8'))
        else:
            error = dict()
        if len(error) == 0:
            error['code'] = resp.reason
            error['message'] = ''
        elif 'error' in error and 'code' in error['error']:
            error = error['error']
        else:
            error['code'] = error['error']
            error['message'] = error['error_description']
        error_response = cls(resp.status_code,
                             error['code'],
                             error['message'])
        return error_response


class MissingRequiredFieldError(Exception):
    pass


class ServerInfoEndpointNotFoundError(Exception):
    pass


class EndpointUnavailableError(Exception):
    pass


class ItemTypeNotAllowed(Exception):
    pass


class NotSignedInError(Exception):
    pass
