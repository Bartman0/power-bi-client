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
    pass

class DatasetRequest(object):
    def post_dataset(self, name, tables):
        return json.dumps({ 'name': name, 'tables': tables })
    def post_rows(self, rows):
        return json.dumps({ 'rows': rows })
    def refresh(self, notify='NoNotification'):
        return json.dumps({ 'notifyOption': notify })


class TableRequest(object):
    def _generate_xml(self, Report_item, connection_credentials=None, connections=None):
        xml_request = ET.Element('tsRequest')
        Report_element = ET.SubElement(xml_request, 'Report')
        Report_element.attrib['name'] = Report_item.name
        if Report_item.show_tabs:
            Report_element.attrib['showTabs'] = str(Report_item.show_tabs).lower()
        project_element = ET.SubElement(Report_element, 'project')
        project_element.attrib['id'] = Report_item.project_id

        if connection_credentials is not None and connections is not None:
            raise RuntimeError('You cannot set both `connections` and `connection_credentials`')

        if connection_credentials is not None:
            _add_credentials_element(Report_element, connection_credentials)

        if connections is not None:
            connections_element = ET.SubElement(Report_element, 'connections')
            for connection in connections:
                _add_connections_element(connections_element, connection)
        return ET.tostring(xml_request)

    def update_req(self, Report_item):
        xml_request = ET.Element('tsRequest')
        Report_element = ET.SubElement(xml_request, 'Report')
        if Report_item.name:
            Report_element.attrib['name'] = Report_item.name
        if Report_item.show_tabs:
            Report_element.attrib['showTabs'] = str(Report_item.show_tabs).lower()
        if Report_item.project_id:
            project_element = ET.SubElement(Report_element, 'project')
            project_element.attrib['id'] = Report_item.project_id
        if Report_item.owner_id:
            owner_element = ET.SubElement(Report_element, 'owner')
            owner_element.attrib['id'] = Report_item.owner_id
        return ET.tostring(xml_request)

    def publish_req(self, Report_item, filename, file_contents, connection_credentials=None, connections=None):
        xml_request = self._generate_xml(Report_item,
                                         connection_credentials=connection_credentials,
                                         connections=connections)

        parts = {'request_payload': ('', xml_request, 'text/xml'),
                 'tableau_Report': (filename, file_contents, 'application/octet-stream')}
        return _add_multipart(parts)

    def publish_req_chunked(self, Report_item, connections=None):
        xml_request = self._generate_xml(Report_item,
                                         connection_credentials=connection_credentials,
                                         connections=connections)

        parts = {'request_payload': ('', xml_request, 'text/xml')}
        return _add_multipart(parts)


class EmptyRequest(object):
    def empty_req(self):
        pass


class RequestFactory(object):
    Empty = EmptyRequest()
    Auth = AuthRequest()
    Capacity = CapacityRequest()
    Dataset = DatasetRequest()
    Table = TableRequest()
