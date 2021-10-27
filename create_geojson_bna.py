import pandas as pd
data = pd.read_excel('Ladesaeulenkarte_Datenbankauszug.xlsx', sheet_name=0, skiprows=5)
data["Max"] = data[["P1 [kW]", "P2 [kW]","P3 [kW]", "P4 [kW]"]].max(axis=1)
freev = data[(data.Betreiber == "ALDI SÜD") |
             (data.Betreiber == "Lidl Dienstleistung GmbH & Co. KG" ) |
             (data.Betreiber == "Kaufland Dienstleistung GmbH & Co. KG")  |
             (data.Betreiber == "deer GmbH")  | 
             (data.Betreiber == "Schwarz Real Estate GmbH & Co. KG")  |
             (data.Betreiber == "IKEA Deutschland GmbH") ]
freev = freev[freev.Max > 10] # Minimum 10 KW
# Create Geojson file
from geojson import Point, Feature, FeatureCollection, dump



features = []

for indice, row in freev.iterrows():
    point = Point(( row["Längengrad"], row["Breitengrad"]))
    features.append(Feature(geometry=point, properties={"Betreiber": row['Betreiber'], "Max_KW" : str(row['Max']) }))

# add more features...
# features.append(...)

feature_collection = FeatureCollection(features)

with open('free_chargers_DE.geojson', 'w') as f:
   dump(feature_collection, f)

