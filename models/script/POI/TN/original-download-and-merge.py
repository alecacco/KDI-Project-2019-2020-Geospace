import requests
import csv
import os
import pandas as pd
import re

# Get urls for datasets and save them into a file

poi_num = requests.get('https://dati.trentino.it/api/3/action/package_search?q=luoghi+e+punti+di+interesse').json()['result']['count']
req = requests.get(f'https://dati.trentino.it/api/3/action/package_search?q=luoghi+e+punti+di+interesse&rows={poi_num}').json()

results = req['result']['results']
resources = {}
for result in results:
    author = result['author']
    for res in result['resources']:
        if res['format'] == 'CSV' and res['name'].startswith('Luoghi'):
            resources[author] = res['url'].replace(' ', '%20')

comuni_df = None
for key, url in resources.items():
    try:
        if key.startswith('Comun') and not key.startswith('Comunit'):
            print(f'Downloading: {key}')
            new = pd.read_csv(url)
            comune = re.sub('Comun((e di)|( general de)) ', '', key).rsplit('.')[0].strip()
            print(f'Comune name: {comune}')
            new['Comune'][:] = comune
            if comuni_df is None:
                comuni_df = new
            else:
                comuni_df = pd.concat([comuni_df, new], axis=0, sort=True)
    except pd.errors.EmptyDataError as e:
        print(f'Empty dataset: {key}')
        print('--------------------------')
    except Exception as e:
        print(e)
        print(key)
        print('--------------------------')

# save datasets

comuni_df.to_csv('./data/datasets/POI/TN/original-dataset-comuni.csv')
