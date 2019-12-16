import xml.etree.ElementTree as ET
import requests as req
import sys
import utm
import pickle
import os

activitypaths = {}
#{' (Escursionisti Esperti)', ' (Turistico)', ' (Escursionisti Esperti con Attrezzatura - Facile)', ' (Escursionisti Esperti con Attrezzatura - Difficile)', ' (Escursionisti Esperti con Attrezzatura - Molto Difficile)', ' (Escursionistico)', ' (Escursionisti Esperti con Attrezzatura - Poco Difficile)'}

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

def invertdata(d,key1,key2):
    temp = d[key1]
    d[key1] = d[key2]
    d[key2] = temp

def do_get_sentieri(command,output_file):
    if command=="SCRAPE":
        source = "https://sentieri.sat.tn.it/schede-sentieri"

        sourceP = req.get(source)
        sourceX = ET.fromstring(gravecleaner(sourceP.text))
        sentieri_names = [e.text for e in sourceX[1][1][0][0][0][0] if e.text!=None]
        print("%d sentieri found"%len(sentieri_names))

        sentieri = {}
        for sentiero_i in range(len(sentieri_names)):
        #for sentiero_i in range(10):
            sentiero_name = sentieri_names[sentiero_i]
            print("Loading %s (%d/%d)"%(sentiero_name,sentiero_i+1,len(sentieri_names)))

            sentieri[sentiero_name] = {
                "page": req.get(
                    source,
                    data={"numero":sentiero_name}
                )
            }
            #sentieri[sentiero_name]["page"].encoding = sentieri[sentiero_name]["page"].apparent_encoding
        tipidifficolta = set()
        for sentiero_i in range(len(sentieri)):
            sentiero = list(sentieri.values())[sentiero_i]
            sentiero["xml"] = ET.fromstring(gravecleaner(sentiero["page"].content.decode("utf-8")))

            #table on the right
            for i in range(len(sentiero["xml"][1][3][0][1][0])):
                key = sentiero["xml"][1][3][0][1][0][i][0].text
                value = sentiero["xml"][1][3][0][1][0][i][1][0].text
                sentiero[key] = value

           #table on the left
            for i in range(len(sentiero["xml"][1][3][0][0][0])):
                key = sentiero["xml"][1][3][0][0][0][i][0].text
                value = sentiero["xml"][1][3][0][0][0][i][1][0].text
                sentiero[key] = value

            #print(list(sentiero["xml"][1][3][0][0][0][2][1].itertext())[1])
            tipidifficolta.add(sentiero["xml"][1][3][0][0][0][2][1][0].text)
            tipidifficolta.add(list(sentiero["xml"][1][3][0][0][0][2][1].itertext())[1])

            #description text box
            """sentiero["Descrizione"] = "\n".join([
                    field
                    for field in sentiero["xml"][1][3][1][0].itertext()
                    if field.split(" ")!=["\n"]
                    ])
            """
            #tabella sotto (solo tappe)
            sentiero["Tappe"] = []
            sentiero["Quote"] = []
            sentiero["Distanze"] = []
            sentiero["Tempi Andata"] = []
            sentiero["Tempi Ritorno"] = []
            sentiero["Agibilità"] = []

            for i in range(len(sentiero["xml"][1][5])-3):
                sentiero["Tappe"].append(sentiero["xml"][1][5][i+1][0][0].text)
                sentiero["Quote"].append(sentiero["xml"][1][5][i+1][1].text)
                sentiero["Distanze"].append(sentiero["xml"][1][5][i+1][2].text)
                if sentiero["xml"][1][5][i+1][3].text!=None:
                    sentiero["Tempi Andata"].append(sentiero["xml"][1][5][i+1][3].text)
                else:
                    sentiero["Tempi Andata"].append("00:00 h")
                if sentiero["xml"][1][5][i+1][4].text!=None:
                    sentiero["Tempi Ritorno"].append(sentiero["xml"][1][5][i+1][4].text)
                else:
                    sentiero["Tempi Ritorno"].append("00:00 h")
                sentiero["Agibilità"].append(sentiero["xml"][1][5][i+1][7].text)

        with open(output_file+".pkl","wb+") as f:
            pickle.dump(sentieri,f)

        #print({k:{kk:vv for kk,vv in v.items() if kk not in ["page","xml"]} for k,v in sentieri.items()})

    else:
        path = os.path.join(os.path.expanduser('~'), output_file+".pkl")
        sentieri = pickle.load(open(path,"rb"))


    f = open(output_file+".csv","w+")
    keys = list(list(sentieri.values())[0].keys())
    keys.remove("page")
    keys.remove("xml")
    f.write((",".join(["Nome"]+["\""+k.replace("\"","'").replace("; ","").replace(":","").replace(";","").replace("à","a").replace("Difficolta","DifficoltaSentiero")+"\"" for k in keys]))+"\n")
    for nome,sentiero in sentieri.items():
        for k in ["Tempo andata:","Tempo ritorno:"]:
            parts = sentiero[k].split(" ")
            if len(parts)>0:
                hm = parts[0].split(":")
                if len(hm)==2:
                    h,m = hm
                    if h.isdigit() and m.isdigit():
                        sentiero[k] = str((60*int(h))+int(m))
                    else:
                        sentiero[k] = 0
                else:
                    sentiero[k] = 0
            else:
                sentiero[k] = 0

        for k in ["Lunghezza:","Tempo andata:","Tempo ritorno:","Quota minima:","Quota massima:","Dislivello salita:","Dislivello discesa:"]:
            sentiero[k] = sentiero[k].replace(" metri","")

        f.write("\""+nome+"_0\"")
        for k in keys:
            f.write(",\""+str(sentiero[k]).replace("\"","'")+"\"")
        f.write("\n")

        invertdata(sentiero,"Tempo andata:","Tempo ritorno:")
        invertdata(sentiero,"Dislivello salita:","Dislivello discesa:")
        invertdata(sentiero,"Località; partenza:","Località; arrivo:")
        toinvert = ["Tappe","Quote","Distanze","Tempi Andata","Tempi Ritorno","Agibilità"]
        for k_to_invert in toinvert:
            sentiero[k_to_invert] = list(reversed(sentiero[k_to_invert]))

        f.write("\""+nome+"_1\"")
        for k in keys:
            f.write(",\""+str(sentiero[k]).replace("\"","'")+"\"")
        f.write("\n")
        
    return(f)  

def rm_main():
    return do_get_sentieri("SCRAPE","sentieri_scraped")

if __name__=="__main__":
    do_get_sentieri(sys.argv[1],sys.argv[2]).close()
