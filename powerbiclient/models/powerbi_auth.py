class PowerBIAuth(object):
    def __init__(self, application_id, application_secret, username, password):
        self.application_id = application_id
        self.application_secret = application_secret
        self.password = password
        self.username = username
