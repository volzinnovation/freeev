# freeev
[A map of free EV charging stations in Germany](https://www.freeev.de)

Currently based on data by [Bundesnetzagentur (BNA)](https://www.bundesnetzagentur.de/DE/Sachgebiete/ElektrizitaetundGas/Unternehmen_Institutionen/E-Mobilitaet/KontaktUndWeiteres.html?nn=971862), which seems incomplete and often incorrect, this analysis is done by [create_map.py](create_map.py) and generates [index.html](index.html) and the file [free_chargers_DE.geojson](free_chargers_DE.geojson)

In progress of merging with data from [OpenStreetMap (OSM)](https://www.openStreetMap.org/). The OSM analysis is [create_map_osm.py](create_map_osm.py) and generates [osm.html](https://www.freeeev.de/osm.html)

Updated occasionally using the fab Github Actions and delivered to the world using Github Pages (and soon CloudFlare).
