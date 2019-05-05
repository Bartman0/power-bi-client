from .attrdict import AttrDict


class Item(AttrDict):
    @classmethod
    def from_response(cls, resp):
        data = resp.json()
        if 'value' in data:
            values = data['value']
        else:
            values = [ data ]
        return [ cls._parse_element(v) for v in values ]

    @classmethod
    def _parse_element(cls, value):
        return cls(value)
