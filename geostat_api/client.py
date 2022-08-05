import requests
from skgstat_uncertainty.models import DataUpload

URL = 'http://localhost:5000/collections/{col_name}/items?f=json'


def get_remote_data(collection_name: str, url: str = URL, json: bool = False) -> DataUpload:
    """get the data from the remote server"""
    r = requests.get(url.format(col_name=collection_name))
    data = r.json()

    # extract the data
    x = [int(f['geometry']['coordinates'][0]) for f in data['features']]
    y = [int(f['geometry']['coordinates'][1]) for f in data['features']]
    v = [float(f['properties']['value']) for f in data['features']]

    meta = {'upload_name': data['metadata']['upload_name'], 'data_type': data['metadata']['data_type']}
    meta['data'] = dict(x=x, y=y, v=v, **{k: v for k,v in data['metadata'].items() if k not in ['upload_name', 'data_type']})

    if json:
        return meta
    else:
        return DataUpload(**meta)
