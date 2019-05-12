from .item import Item


class ReportItem(Item):
    @classmethod
    def from_response(cls, resp, app=None):
        data = resp.json()
        if 'value' in data:
            values = data['value']
        else:
            values = [ data ]
        if app is None:
            return values
        result = []
        for v in values:
            v['app_id'] = app.id        # add parent app.id to every dashboard item
            result.append(cls._parse_element(v))
        return result
