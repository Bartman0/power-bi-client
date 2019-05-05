from .item import Item


class TableItem(Item):
    @classmethod
    def from_response(cls, dataset, resp):
        data = resp.json()
        if 'value' in data:
            values = data['value']
        else:
            values = [ data ]
        result = []
        for v in values:
            v['dataset_id'] = dataset.id        # add parent dataset.id to every table item
            result.append(cls._parse_element(v))
        return result
