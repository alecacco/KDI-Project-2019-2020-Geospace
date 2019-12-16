import os
import pandas as pd
from translate import Translator

AZURE_SECRET_ACCESS_KEY = os.environ['AZURE_SECRET_ACCESS_KEY']

map_types = {
    "Chiesa": "PointOfInterest",
    "Palazzo": "Attraction",
    "Forte": "Attraction",
    "Parco naturale": "Attraction",
    "Biblioteca": "PointOfInterest",
    "Ufficio postale": "PointOfInterest",
    "Scuola infanzia": "PointOfInterest",
    "Scuola elementare": "PointOfInterest",
    "Piscina": "Attraction",
    "Trasporti": "PointOfInterest",
    "Centro sportivo": "Attraction",
    "Museo": "Attraction",
    "Sito storico": "Attraction",
    "Castello": "Attraction",
    "Carabinieri": "PointOfInterest",
    "Vigili del fuoco": "PointOfInterest",
    "Pronto soccorso": "EmergencyService",
    "Sci aplinismo / Sci Escursionismo": "Attraction",
    "Scuola di sci": "Attraction",
    "Ambulatorio": "EmergencyService",
    "RSA (Residenza Sanitaria Assistenziale)": "EmergencyService",
    "Nido infanzia": "PointOfInterest",
    "Scuola (media o secondaria)": "PointOfInterest",
    "Località turistica": "Attraction",
    "Via o piazza": "Attraction",
    "Centro di associazione (musica, teatro...)": "Attraction",
    "Frazione": "Attraction",
    "Biotopo": "Attraction",
    "Monte": "Attraction",
    "Farmacia": "EmergencyService",
    "Polizia": "PointOfInterest",
    "Stadi - campi da calcio": "Attraction",
    "Bocciodromo": "Attraction",
    "Parco giochi": "Attraction",
    "Arrampicate": "Attraction",
    "Mountain Bike": "Attraction",
    "Luogo incantevole": "Attraction",
    "Luogo religioso": "PointOfInterest",
    "Rovine": "Attraction",
    "Monumento": "Attraction",
    "Sito Archeologico": "Attraction",
    "Polizia locale": "PointOfInterest",
    "Teatro": "Attraction",
    "Lago": "Attraction",
    "Varie": "PointOfInterest",
    "Ciclismo": "Attraction",
    "Malga": "PointOfInterest",
    "Mercato": "Shop",
    "Parco avventura": "Attraction",
    "Alpinismo": "Attraction",
    "Vela/Windsurf": "Attraction",
    "Patrocinato sindacale": "PointOfInterest",
    "Centro diurno": "PointOfInterest",
    "Ferrata": "Attraction",
    "Pista ciclabile": "Attraction",
    "Snow park": "Attraction",
    "Trekking": "Attraction",
    "Luogo Religioso": "PointOfInterest",
    "Ecomuseo": "Attraction",
    "Parcheggio": "PointOfInterest",
    "Parchi e orti botanici": "Attraction",
    "Percorso naturalistico": "Attraction",
    "Musei": "Attraction",
    "Area archeologica": "Attraction",
    "Altri siti di interesse storico artistico": "Attraction",
    "Natura": "Attraction",
    "Edificio storico": "Attraction",
    "Parchi e giardini": "Attraction",
    "Impianto sportivo multidisciplinare": "Attraction",
    "Poligono di tiro": "Attraction",
    "Campo da tennis": "Attraction",
    "Campo da calcio": "Attraction",
    "Casa di riposo": "EmergencyService",
    "Centro di equitazione": "Attraction",
    "Alloggio protetto": "PointOfInterest",
    "Nido d'infanzia": "PointOfInterest",
    "Scuola d'infanzia": "PointOfInterest",
    "Centro infanzia": "PointOfInterest",
    "Polo sociale": "PointOfInterest",
    "CRM": "PointOfInterest",
    "Info point": "PointOfInterest",
    "Punto allattamento / cambio": "PointOfInterest",
    "Altri siti di interesse turistico": "Attraction",
    "Spazio di aggregazione ": "PointOfInterest",
    "Dolomiti": "Attraction",
    "Etnografia": "PointOfInterest",
    "Cascate": "Attraction",
    "Monumento naturale": "Attraction",
    "Tennis": "Attraction",
    "Sanità": "EmergencyService",
    "Canyon/Grotte": "Attraction",
    "Bottega storica": "Shop",
    "Punto di interesse": "PointOfInterest",
    'Area faunistica': "Attraction",
    'Associazione': "PointOfInterest",
    'Canoa/Kayak': "Attraction",
    'Canyoning': "Attraction",
    'Ciclabili': "Attraction",
    'Downhill Bike Park': "Attraction",
    'Equitazione': "Attraction",
    'Esposizione/Galleria': "Attraction",
    'Fiumi e torrenti': "Attraction",
    'Ghiacciaio': "Attraction",
    'Golf': "Attraction",
    'Ice Climbing': "Attraction",
    'Infrastrutturazione turistica': "PointOfInterest",
    'Noleggio attrezzature sportive': "Attraction",
    'Nordic Walking': "Attraction",
    'Parapendio/Deltaplano': "Attraction",
    'Rafting': "Attraction",
    'Sci alpinismo / Sci Escursionismo': "Attraction",
    "Tiro con l'arco": "Attraction",
    'Via Claudia Augusta': "Attraction",
    'Piste da sci': "Attraction",
    'Ciaspolata': "Attraction",
    'Pattinaggio sul ghiaccio': "Attraction"
}

translator = Translator(provider='microsoft', from_lang='it', to_lang='en', secret_access_key=AZURE_SECRET_ACCESS_KEY)
trans_types = {}
for t in map_types:
    trans_types[t] = translator.translate(t)

comuni_df = pd.read_csv('./data/datasets/POI/TN/cleaned-full-dataset-comuni.csv')
comuni_df['Tipologia di luogo'] = comuni_df['Tipologia di luogo'].fillna('Punto di interesse')
comuni_df['Type'] = comuni_df.apply(lambda x: map_types[x['Tipologia di luogo']], axis=1)
comuni_df['Tipologia di luogo en'] = comuni_df.apply(lambda x: trans_types[x['Tipologia di luogo']], axis = 1)

POI_df = comuni_df[comuni_df['Type'] == 'PointOfInterest']
attraction_df = comuni_df[comuni_df['Type'] == 'Attraction']
shop_df= comuni_df[comuni_df['Type'] == 'Shop']
emergency_df = comuni_df[comuni_df['Type'] == 'EmergencyService']

POI_df.to_csv('./data/datasets/POI/TN/final-datasets/PointOfInterest.csv')
attraction_df.to_csv('./data/datasets/POI/TN/final-datasets/Attraction.csv')
shop_df.to_csv('./fdata/POI/TN/inal-datasets/Shop.csv')
emergency_df.to_csv('./data/datasets/POI/TN/final-datasets/EmergencyService.csv')