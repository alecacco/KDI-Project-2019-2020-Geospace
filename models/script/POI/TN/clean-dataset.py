from bs4 import BeautifulSoup
from html import unescape
import numpy as np
import os
import pandas as pd
from postal.parser import parse_address
from translate import Translator

# Utilities

def clean_text(el):
    return el if type(el) == float else BeautifulSoup(unescape(el), "lxml").text

def getAddressValue(col, address):
    if type(address) is not float or not np.isnan(address):
        address_dict = {k: v for (v, k) in parse_address(address)}
        res = address_dict.get(col)
        return str(res) if res is not None else np.nan
    return np.nan
    

comuni = pd.read_csv('./data/datasets/POI/TN/original-dataset-comuni.csv')

# filter by lat and lon inside Trentino

comuni_clean = comuni[((comuni['lon'] >= 10.41) & (comuni['lon'] <= 11.97) & (comuni['lat'] >= 45.60) & (comuni['lat'] <= 46.60)) | (comuni['Titolo']=='Lago di Garda')]
comuni_clean = comuni_clean[(comuni_clean['Tipologia di luogo'] != 'Sentieri e Itinerari') & (comuni_clean['Tipologia di luogo'] != 'Sentieri e itinerari') & (comuni_clean['Tipologia di luogo'] != 'Rifugio') & (comuni_clean['Tipologia di luogo'] != 'Percorso')]

for col in comuni_clean.select_dtypes(include=[object]):
    try:
        comuni_clean[col] = comuni_clean[col].apply(clean_text)
    except:
        print(f'Error in {col}')

comuni_clean['Province'] = comuni_clean.apply(lambda x: 'TN', axis=1)
comuni_clean['Street'] = comuni_clean.apply(lambda x: getAddressValue('road', x['address']), axis=1)
comuni_clean['Number'] = comuni_clean.apply(lambda x: getAddressValue('house_number', x['address']), axis=1)
comuni_clean['CAP'] = comuni_clean.apply(lambda x: getAddressValue('postcode', x['address']), axis=1)

comuni_clean.to_csv('./data/datasets/POI/TN/cleaned-full-dataset-comuni.csv')