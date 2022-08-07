import os
from pygeoapi.provider.base import BaseProvider

from skgstat_uncertainty.api import API
from skgstat_uncertainty.models import DataUpload

from geostat_api import DATA_PATH, DB_NAME


def extract_features(dataset: DataUpload):
    features = []
    data = dataset.data
    for i, (x, y, v) in enumerate(zip(data['x'], data['y'], data['v'])):    
        f = {
            'type': 'Feature',
            'id': i,
            'geometry': {
                'type': 'Point',
                'coordinates': [x, y]
            },
            'properties': {
                'value': v,
                'x': x,
                'y': y
                
            }
        }
        features.append(f)

    return features

class DataUploadProvider(BaseProvider):
    """connect to our database and load data"""
    def __init__(self, provider_def):
        BaseProvider.__init__(self, provider_def)

        # create the api
        self.api = API(data_path=DATA_PATH, db_name=DB_NAME)

        # load the dataset
        self.dataset = self.api.get_upload_data(id=self.data)
        self.features = extract_features(self.dataset)

    def query(self, startindex=0, limit=100, **kwargs):

        # get the features
        features = self.features#[startindex:limit]
        meta = dict(
            upload_name=self.dataset.upload_name,
            data_type=self.dataset.data_type,
            **{k: v for k, v in self.dataset.data.items() if k not in ['x', 'y', 'v', 'field']}
        )
        geojson = {
            'type': 'FeatureCollection',
    '       features': features,
            'metadata': meta
        }

        return geojson

    def get(self, identifier=None, **kwargs):
        return [f for f in self.features if f['id'] == int(identifier)].pop()
