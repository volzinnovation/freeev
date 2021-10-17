import pandas as pd
data = pd.read_excel('Ladesaeulenkarte_Datenbankauszug.xlsx', sheet_name=0, skiprows=5)
data["Max"] = data[["P1 [kW]", "P2 [kW]","P3 [kW]", "P4 [kW]"]].max(axis=1)
freev = data[(data.Betreiber == "ALDI SÜD") |
             (data.Betreiber == "Lidl Dienstleistung GmbH & Co. KG" ) |
             (data.Betreiber == "Kaufland Dienstleistung GmbH & Co. KG")  |
             (data.Betreiber == "deer GmbH")  | 
             (data.Betreiber == "Schwarz Real Estate GmbH & Co. KG")  |
             (data.Betreiber == "IKEA Deutschland GmbH") ]
freev = freev[freev.Max > 22]
# Create map
import folium
from folium.plugins import LocateControl
title = 'Kostenfreie deutsche Ladesäulen'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b><br/><i>Tipp:Auf Markierung klicken, um zur Ladestation zu navigieren.</i></h3>
             '''.format(title)   
mymap = folium.Map(location=[49.0, 8.2], zoom_start=9)
mymap.get_root().html.add_child(folium.Element(title_html))
LocateControl(True).add_to(mymap)
#You Markler the point in Map
for indice, row in freev.iterrows():
    folium.CircleMarker(
        location=[row["Breitengrad"],row["Längengrad"] ],
        popup = '<a href="https://www.google.com/maps/search/?api=1&query=' + str(row["Breitengrad"]) + "," + str(row["Längengrad"]) +'">' + row['Betreiber'] + ' (' + str(row['Max']) + ' KW)' + '</a>',
        tooltip=row['Betreiber'] + ' (' + str(row['Max']) + ' KW)', # https://www.google.com/maps/search/?api=1&query=48.80506,8.4449
        icon=folium.map.Icon(color='blue')
    ).add_to(mymap)
mymap.save("index.html")
