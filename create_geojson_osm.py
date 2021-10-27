# Import Python libraries
import osmium as o
import sys
import pandas as pd
import numpy as np

# List charging stations found in OpenStreetMap data dump
lats = []
lons = []
names = []
kws = []

def add(lat,lon,name,kw):
  lats.append(lat)
  lons.append(lon)
  names.append(name)
  kws.append(kw)
  print(".")

class CSHandler(o.SimpleHandler):

  def node(self, n):
     if n.tags.get('amenity') == 'charging_station' and n.tags.get('fee') == "no" and  n.tags.get('socket:type2') =='1':
        name = n.tags.get('operator', '')
        kw = n.tags.get('socket:type2:output', '?')
        add("%f" % n.location.lat, "%f" % n.location.lon, "%s" % name, "%s" % kw ) # due to strange errors in pyosmium
        del n # due to strange errors in pyosmium
        

# Parse and Filter data
handler = CSHandler()
handler.apply_file("osm.pbf")

# Create data frame from results
cs = pd.DataFrame({
                            'Längengrad': lons,
                            'Breitengrad'  : lats,
                            'Betreiber' : names,
                            'Max' : kws
                           })
cs.describe()

#Create Geojson file
from geojson import Point, Feature, FeatureCollection, dump



features = []

for indice, row in cs.iterrows():
    point = Point(( row["Längengrad"], row["Breitengrad"]))
    features.append(Feature(geometry=point, properties={"Betreiber": row['Betreiber'], "Max_KW" : str(row['Max']) }))

feature_collection = FeatureCollection(features)

with open('free_chargers_OSM.geojson', 'w') as f:
   dump(feature_collection, f)

