import logging

from ..request_factory import RequestFactory
from .endpoint import api, Endpoint
from .. import GroupItem, UserItem

logger = logging.getLogger('powerbi.endpoint.groups')


class Groups(Endpoint):
    def __init__(self, parent_srv):
        super(Groups, self).__init__(parent_srv)

    @property
    def baseurl(self):
        return "{0}/groups".format(self.parent_srv.baseurl)

    # get all groups
    @api(version="1.0")
    def get(self, req_options=None, filter=None):
        logger.info('querying all groups')
        if filter is None:
            url = self.baseurl
        else:
            url = "{0}?{1}".format(self.baseurl, filter)    # TODO: make a filter class
        server_response = self.get_request(url, req_options)
        all_group_items = GroupItem.from_response(server_response)
        return all_group_items

    # get all users in group
    @api(version="1.0")
    def get_users(self, group, req_options=None):
        if not group or not group.id:
            error = "group ID undefined"
            raise ValueError(error)
        logger.info('querying all users in group')
        url = "{0}/{1}/users".format(self.baseurl, group.id)
        server_response = self.get_request(url, req_options)
        all_user_items = UserItem.from_response(server_response)
        return all_user_items

    # create group
    @api(version="1.0")
    def create(self, name, req_options=None):
        if not name:
            error = "group name undefined"
            raise ValueError(error)
        url = self.baseurl
        post_req = RequestFactory.Group.create(name)
        server_response = self.post_request(url, post_req, req_options)
        logger.info('created group (name: {0})'.format(name))
        all_group_items = GroupItem.from_response(server_response)
        return all_group_items

    # delete group
    @api(version="1.0")
    def delete(self, group, req_options=None):
        if not group or not group.id:
            error = "group ID undefined"
            raise ValueError(error)
        url = "{0}/{1}".format(self.baseurl, group.id)
        self.delete_request(url, req_options)
        logger.info('deleted group (ID: {0})'.format(group.id))

    # add user to group
    @api(version="1.0")
    def add_user(self, group,
                 display_name, email_address, group_user_access_right, identifier, principal_type,
                 req_options=None):
        if not group or not group.id:
            error = "group ID undefined"
            raise ValueError(error)
        url = "{0}/{1}/users".format(self.baseurl, group.id)
        add_req = RequestFactory.Group.add(display_name, email_address, group_user_access_right, identifier, principal_type)
        self.post_request(url, add_req, req_options)
        logger.info('added user (ID: {0}) to group (ID: {1})'.format(identifier, group.id))

    # add user to group
    @api(version="1.0")
    def delete_user(self, group, user_id, req_options=None):
        if not group or not group.id:
            error = "group ID undefined"
            raise ValueError(error)
        if not user_id:
            error = "user ID undefined"
            raise ValueError(error)
        url = "{0}/{1}/users/{2}".format(self.baseurl, group.id, user_id)
        self.post_request(url, req_options)
        logger.info('delete user (ID: {0}) to group (ID: {1})'.format(user_id, group.id))
