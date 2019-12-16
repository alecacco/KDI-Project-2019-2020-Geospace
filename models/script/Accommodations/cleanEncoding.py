import sys
import os
import json
from postal.parser import parse_address


def get_value(key, collection):
    for (v, k) in collection:
        if k == key:
            return v
    return ''


def rm_main():
    path = os.path.join(os.path.expanduser('~'), 'hotels.json')
    outputFile = open("hotels.csv", "a")
    header = 'name,type,city,street,number,cap,lat,lon,checkin_from,checkin_to,checkout_from,checkout_to,description,score,num_reviews,Animali,Parcheggio,Internet,Servizi benessere,Servizi di ristorazione\n'

    outputFile.write(header)
    with open(path, encoding='unicode-escape') as f:
        hotels = json.load(f)
        for hotel in hotels:
            array = []
            for i in hotel:
                if i == 'address':
                    addrfromess = parse_address(str(hotel[i]))
                    array.append(get_value('city', addrfromess))
                    array.append(get_value('road', addrfromess))
                    array.append(get_value('house_number', addrfromess))
                    array.append(get_value('postcode', addrfromess))
                elif i == 'score':
                    array.append(str(hotel[i]).replace(',', '.'))
                else:
                    array.append(str(hotel[i]).replace(',', ''))
            row = ','.join(array)
            outputFile.write(row + '\n')
        return outputFile
