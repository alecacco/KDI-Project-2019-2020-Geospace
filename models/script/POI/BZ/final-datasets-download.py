from bs4 import BeautifulSoup
import html
import json
import requests

poi_separated = {
    'PointOfInterest': [],
    'Attraction': [],
    'Shop': [],
    'EmergencyService': [],
    'Restaurant': []    
}

base_poi_url = 'http://tourism.opendatahub.bz.it/api/Poi'

##### PointOfInterest

# Get the number of services POI
service_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=128&active=true').json()['TotalResults']
# Download all of them by setting the pagesize parameter to service_num
if service_num > 0:
    service_poi = requests.get(base_poi_url + '?pagenumber=1&poitype=128&active=true&pagesize=' + str(service_num)).json().get('Items')
    poi_separated['PointOfInterest'] += service_poi if service_poi is not None else []

public_poi_subtypes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 1024]
for sub_type in public_poi_subtypes:
    sub_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=16&subtype=' + str(sub_type) + '&active=true').json()['TotalResults']
    if sub_num > 0:
        sub_dict = requests.get(base_poi_url + '?pagenumber=1&poitype=16&subtype=' + str(sub_type) + '&active=true&pagesize=' + str(sub_num)).json().get('Items')
        poi_separated['PointOfInterest'] += sub_dict if sub_dict is not None else []

traffic_poi_subtypes = [2, 4, 8, 64, 128, 256, 512, 1024]
for sub_type in traffic_poi_subtypes:
    sub_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=64&subtype=' + str(sub_type) + '&active=true').json()['TotalResults']
    if sub_num > 0:
        sub_dict = requests.get(base_poi_url + '?pagenumber=1&poitype=64&subtype=' + str(sub_type) + '&active=true&pagesize=' + str(sub_num)).json().get('Items')
        poi_separated['PointOfInterest'] += sub_dict if sub_dict is not None else []

##### Attraction

culture_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=4&active=true').json()['TotalResults']
if culture_num > 0:
    culture_r = requests.get(base_poi_url + '?pagenumber=1&poitype=4&active=true&pagesize=' + str(culture_num)).json().get('Items')
    poi_separated['Attraction'] += culture_r if culture_r is not None else []
    
sports_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=32&active=true').json()['TotalResults']
if sports_num > 0:
    sports_r = requests.get(base_poi_url + '?pagenumber=1&poitype=32&active=true&pagesize=' + str(sports_num)).json().get('Items')
    poi_separated['Attraction'] += sports_r if sports_r is not None else []

nights_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=8&active=true').json()['TotalResults']
if nights_num > 0:
    nights_r = requests.get(base_poi_url + '?pagenumber=1&poitype=8&active=true&pagesize=' + str(nights_num)).json().get('Items')
    poi_separated['Attraction'] += nights_r if nights_r is not None else []

##### Shop 

shop_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=2&active=true').json()['TotalResults']
if shop_num > 0:
    shop_r = requests.get(base_poi_url + '?pagenumber=1&poitype=2&active=true&pagesize=' + str(shop_num)).json().get('Items')
    poi_separated['Shop'] += shop_r if shop_r is not None else []

craft_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=256&subtype=512&active=true').json()['TotalResults']
if craft_num > 0:
    craft_r = requests.get(base_poi_url + '?pagenumber=1&poitype=256&active=true&pagesize=' + str(craft_num)).json().get('Items')
    poi_separated['Shop'] += craft_r if craft_r is not None else []

##### EmergencyService

emergency_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=1&active=true').json()['TotalResults']
if emergency_num > 0:
    emergency_r = requests.get(base_poi_url + '?pagenumber=1&poitype=1&active=true&pagesize=' + str(emergency_num)).json().get('Items')
    poi_separated['EmergencyService'] += emergency_r if emergency_r is not None else []

hospitals_num = requests.get(base_poi_url + '?pagenumber=1&pagesize=10&poitype=16&subtype=512&active=true').json()['TotalResults']
if hospitals_num > 0:
    hospitals_r = requests.get(base_poi_url + '?pagenumber=1&poitype=16&subtype=512&active=true&pagesize=' + str(hospitals_num)).json().get('Items')
    poi_separated['EmergencyService'] += hospitals_r if hospitals_r is not None else []

##### Restaurant

restaurant_num = requests.get('http://tourism.opendatahub.bz.it/api/Gastronomy?pagenumber=1&pagesize=10&active=true').json()['TotalResults']
if restaurant_num > 0:
    restaurants = requests.get('http://tourism.opendatahub.bz.it/api/Gastronomy?pagenumber=1&pagesize=' + str(restaurant_num) + '&active=true').json().get('Items')
    poi_separated['Restaurant'] += restaurants if restaurants is not None else []

for key in poi_separated:
    with open(f'./data/datasets/POI/BZ/final-datasets/{key}.json', 'w') as fp:
        tmp = json.dumps(poi_separated[key])
        tmp = html.unescape(tmp)
        tmp = BeautifulSoup(tmp, "lxml").text
        fp.write(tmp)
        fp.close()