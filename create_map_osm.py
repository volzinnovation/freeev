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

# Create Map
import folium
from folium.plugins import LocateControl
loc = 'Kostenfreie deutsche Ladesäulen'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b><br/><i>Tipp:Auf Markierung klicken, um zur Ladestation zu navigieren.<br/>Info: Basis sind Daten der OpenStreetMap.</i></h3>
             '''.format(loc)   
mymap = folium.Map(location=[49.0, 8.2], zoom_start=9)
mymap.get_root().html.add_child(folium.Element(title_html))
LocateControl(True).add_to(mymap)
#You Markler the point in Map
for indice, row in cs.iterrows():
    color='lightblue'
    # if(float(row['Max']) > 49): color='blue'
    folium.Marker(
        location=[float(row["Breitengrad"]),float(row["Längengrad"]) ],
        popup = '<a href="https://www.google.com/maps/search/?api=1&query=' + str(row["Breitengrad"]) + "," + str(row["Längengrad"]) +'">' + row['Betreiber'] + '(' + str(row['Max']) + ')' + '</a>',
        tooltip=row['Betreiber'] + '(' + str(row['Max']) + ')', # https://www.google.com/maps/search/?api=1&query=48.80506,8.4449
        icon=folium.map.Icon(color=color)
    ).add_to(mymap)

mymap.save("osm.html")
