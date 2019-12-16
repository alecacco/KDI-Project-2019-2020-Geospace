from lxml import html
import requests as req
import sys
import json
import pickle
import os

def gravecleaner(s):
    res = s

    replacements = {
        "&agrave":"à",
        "&egrave":"è",
        "&igrave":"ì",
        "&ograve":"ò",
        "&ugrave":"ù",
        "&nbsp":" ",
        "&copy":""
    }
    for k,v in replacements.items():
        res = res.replace(k,"à")

    return res

def parse_period(s):

    months_it = {
        "gennaio":  str(1),
        "febbraio": str(2),
        "marzo":    str(3),
        "aprile":   str(4),
        "maggio":   str(5),
        "giugno":   str(6),
        "luglio":   str(7),
        "agosto":   str(8),
        "settembre":str(9),
        "ottobre":  str(10),
        "novembre": str(11),
        "dicembre": str(12)
    }

    parts = s.split(" - ")
    if len(parts) == 2:
        open_split = parts[0].split(" ")
        close_split = parts[1].split(" ")
        if len(open_split)==2 and len(close_split)==2:
            opening_day, opening_month = open_split
            closing_day, closing_month = close_split
            if opening_day.isdigit() and closing_day.isdigit() and opening_month in months_it.keys() and closing_month in months_it.keys():
                return [opening_day+"/"+months_it[opening_month] , closing_day+"/"+months_it[closing_month]]

    return ["",""]

"""
source = "https://www.sat.tn.it/rifugi/elenco-rifugi/show"
#sourceP = req.get(source).content.decode("utf-8"))

rifugio = 1
rifugioResponse = req.get(source,params={"id_rifugio":str(rifugio)})
rifugi = {}
while rifugioResponse.status_code == 200:
    doc = lxml.html.fromstring(rifugioResponse.content)
    name = doc.xpath("//div[@id='showRifugio']/h1/text()")[0]
    print("scraping "str(name)
    rifugio[name] = {

    }

    rifugio+=1
    rifugioResponse = req.get(source,params={"id_rifugio":str(rifugio)})
"""

def do_get_rifugi(command,output_file):

    if command=="SCRAPE":
        coordsource = "https://api.webmapp.it/trentino/geojson/rifugi.geojson"

        coordsResponse = req.get(coordsource)

        coordsJson = json.loads(coordsResponse.text)

        huts = []

        hutkeys = set()
        rif_id = 0
        for hut in coordsJson["features"]:#[:3]:
            hutReq = req.get("http://"+hut["properties"]["website"])
            hutPage = html.fromstring(hutReq.content)
            
            hutData = {}
            hutData["name"] = hutPage.xpath("//div[@id='showRifugio']/h1/text()")[0]
            print("scraping "+str(hutData["name"]))

            table1 = hutPage.xpath("//div[@id='showRifugio-tabs-1']")[0][0]
            for row in table1:
                if len(row)==2:
                    hutkeys.add(row[0].text)
                    print(row[0].text+" --> "+(row[1].text if row[1].text!=None else "EMPTY"))
                    hutData[row[0].text] = "\"" + (row[1].text.replace("\"","'")  if row[1].text!=None else "") + "\""

            if len(hutPage.xpath("//div[@id='showRifugio-tabs-2']")[0][1])>0:
                desc = hutPage.xpath("//div[@id='showRifugio-tabs-2']")[0][1][0].text 
            else:
                desc = ""
            print("DESC --> "+desc if desc!="" else "No Description")
            hutData["Description"] = "\"" + desc.replace("\"","'")+ "\""

            print("\n"+"-"*20+"\n")

            #=====================
            goodhut = {
                "id" : rif_id,
                "lat" : hut["properties"]["coordinates"].split(", ")[0][2:],
                "lon" : hut["properties"]["coordinates"].split(", ")[1][2:],
                "altitude" : hutData["Quota"][1:-1].replace(" m",""),
                "name" : hutData["name"],
                "website" : hutData["Web"][1:-1],
                "mail" : hutData["E-mail"][1:-1],
                "phones" : "-".join([hutData["Telefono gestore"][1:-1],hutData["Telefono rifugio"][1:-1]]),
                "description" : hutData["Description"][1:-1].replace("\"","").replace("\n",""),
                "vote" : 5,
                "number_votes" : 1,
                "tags" : "mountain, hut, hiking",
                "price" : "",
                "type" : "MountainHut",
                "food" : hutData["Ristorante"]=="Si",
                "parking" : False,
                "animals": True,
                "internet": False,
                "wellness": False
            }

            opening = parse_period(hutData["Apertura"][1:-1])
            goodhut["opening"] = parse_period(hutData["Apertura"][1:-1])[0]
            goodhut["closing"] = parse_period(hutData["Apertura"][1:-1])[1]

            if len(hutData["Posti letto totale"][1:].split(" "))>0:
                if hutData["Posti letto totale"][1:].split(" ")[0].isdigit():
                    goodhut["beds"] = hutData["Posti letto totale"][1:].split(" ")[0]
                else:
                    goodhut["beds"] = ""
            else:
                goodhut["beds"] = ""

            huts.append(goodhut)
        
            rif_id += 1

        print(hutkeys)

        with open(os.path.join(os.path.expanduser('~'), output_file+".pkl"),"wb+") as f:
            pickle.dump(huts,f)

    else:
        path = os.path.join(os.path.expanduser('~'), output_file+".pkl")
        huts = pickle.load(open(path,"rb"))

    f = open(os.path.join(os.path.expanduser('~'), output_file+".csv"),"w+")
    #do parse dict and output csv

    keys = list(huts[0].keys())
    f.write(",".join(keys)+"\n")
    for hut in huts:
        f.write(",".join(["\""+str(hut[k]).replace("\"","'")+"\"" for k in keys]))
        f.write("\n")

    return f

def rm_main():
    return do_get_rifugi("LOAD","rif_scraped")

if __name__=="__main__":
    do_get_rifugi(sys.argv[1],sys.argv[2]).close()
