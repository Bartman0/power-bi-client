from .item import Item


class WorkloadItem(Item):
    @classmethod
    def from_response(cls, resp, capacity=None):
        data = resp.json()
        if 'value' in data:
            values = data['value']
        else:
            values = [ data ]
        result = []
        for v in values:
            v['capacity_id'] = capacity.id        # add parent capacity.id to every workload item
            result.append(cls._parse_element(v))
        return result
