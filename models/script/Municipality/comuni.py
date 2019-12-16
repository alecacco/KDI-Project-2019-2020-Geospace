import pandas as pd
import requests
def rm_main():
    data = pd.read_csv('~/Desktop/Comuni2019Clean.csv', encoding='UTF-8', sep=';')
    # Done by RapidMinor
    # to_keep = (data['Sigla automobilistica'] == "TN") | (data['Sigla automobilistica'] == "BZ")
    # data = data[to_keep]
    # out['lat'] = out.apply(getcoords("lat"), axis=1)
    # out['lon'] = out.apply(getcoords("lon"), axis=1)
    data['lat'] = data.apply(lambda row: requests.get('https://nominatim.openstreetmap.org/search?city='
                                                      + row['Denominazione in italiano'] + '&county=Trentino&format=json').json()[0]['lat'], axis=1)
    data['lon'] = data.apply(lambda row: requests.get('https://nominatim.openstreetmap.org/search?city='
                                                      + row['Denominazione in italiano'] + '&county=Trentino&format=json').json()[0]['lon'], axis=1)

    f = open("comuni_out.csv","w+")
    f.write(data.to_csv())
    return f
