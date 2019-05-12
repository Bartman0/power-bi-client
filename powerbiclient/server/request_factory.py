import json


class AuthRequest(object):
    def signin_req(self, auth_item):
        data = {
            'grant_type': 'password',
            'scope': 'openid',
            'resource': "https://analysis.windows.net/powerbi/api",
            'client_id': auth_item.application_id,
            'client_secret': auth_item.application_secret,
            'username': auth_item.username,
            'password': auth_item.password
        }
        return data


class CapacityRequest(object):
    @classmethod
    def patch_workload(cls, state, maxMemoryPercentageSetByUser):
        return json.dumps({ 'state': state, 'maxMemoryPercentageSetByUser': maxMemoryPercentageSetByUser })


class DatasetRequest(object):
    @classmethod
    def post_dataset(cls, name, tables):
        return json.dumps({ 'name': name, 'tables': tables })
    @classmethod
    def post_rows(cls, rows):
        return json.dumps({ 'rows': rows })
    @classmethod
    def refresh(cls, notify='NoNotification'):
        return json.dumps({ 'notifyOption': notify })


class GroupRequest(object):
    @classmethod
    def create(cls, name):
        return json.dumps({ 'name': name })
    @classmethod
    def add(cls, display_name, email_address, group_user_access_right, identifier, principal_type):
        return json.dumps({ 'displayName': display_name,
                            'emailAddress': email_address,
                            'groupUserAccessRight': group_user_access_right,
                            'identifier': identifier,
                            'principalType': principal_type })


class ReportRequest(object):
    @classmethod
    def clone(cls, name, target_model_id=None, target_workspace_id=None):
        req = {'name': name }
        if target_model_id is not None:
            req['targetModelId'] = target_model_id
        if target_model_id is not None:
            req['targetWorkspaceId'] = target_workspace_id
        return json.dumps(req)


class RequestFactory(object):
    Auth = AuthRequest()
    Capacity = CapacityRequest()
    Dataset = DatasetRequest()
    Group = GroupRequest()
    Report = ReportRequest()
