import csv


def load_csv(filename):
    """
    {
        'sku-region': {
            'sku': 123456,
            'name': 'Name',
            'category': Category,
            'events': [
                {'date': '2017-04-14...', 'in_stock': 0},
                {'date': '2017-04-16...', 'in_stock': 1}
            ]
        }
    }
    """
    data = {}
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = '%s-%s' % (row['sku'], row['region'])
            if not data.get(key):
                sku = row['sku']
                name = row['name']
                category = row['category']
                data[key] = {
                    'sku': int(sku),
                    'name': name,
                    'category': category,
                    'events': list()
                }
            event = {
                'date': row['date'],
                'in_stock': int(row['in_stock'])
            }
            data[key]['events'].append(event)

    # Sort the events by date
    for k, v in data.iteritems():
        data[k]['events'] = sorted(v['events'], key=lambda x: x['date'])
    return data
