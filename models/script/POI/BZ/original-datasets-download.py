import json
import requests

base_url = 'https://tourism.opendatahub.bz.it/api/Poi?active=true'
n_poi = requests.get(base_url).json()['TotalResults']
raw_poi_data = requests.get(f'{base_url}&pagesize={n_poi}').json()
with open('./data/datasets/POI/BZ/original-datasets/poi_bz.json', 'w+') as f:
    json.dump(raw_poi_data['Items'], f)
    f.close()

restaurants_url = 'https://tourism.opendatahub.bz.it/api/Gastronomy?active=true'
n_restaurants = requests.get(restaurants_url).json()['TotalResults']
raw_restaurant_data = requests.get(f'{restaurants_url}&pagesize={n_restaurants}').json()
with open('./data/datasets/POI/BZ/original-datasets/restaurants_bz.json', 'w+') as f:
    json.dump(raw_restaurant_data['Items'], f)
    f.close()