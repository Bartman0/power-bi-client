from .item import Item


class ReportItem(Item):
    @classmethod
    def from_response(cls, app, resp):
        data = resp.json()
        if 'value' in data:
            values = data['value']
        else:
            values = [ data ]
        result = []
        for v in values:
            v['app_id'] = app.id        # add parent app.id to every dashboard item
            result.append(cls._parse_element(v))
        return result
