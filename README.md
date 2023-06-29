# Ulysses-Machine-Learning
Uses machine learning to map all locations in the novel Ulysses by James Joyce using Spacy. My Cardiff University final year project involved creating a web application that allowed a user to map the places mentioned in Ulysses by the famous author James Joyce with (supervised) machine learning. The system used named entity recognition (NER) and geocoding software provided by SpaCy and the GeoPy libraries respectively to identify and geocode locations mentioned in Ulysses. The locations were plotted on a map (using a background map such as that of OpenStreetMap with the use of Folium, a leaflet python library).

Live Demo - https://users.cs.cf.ac.uk/Anyiam-OsigweCE1/Ulysses_website/ul_home.html

Produce a file containing all place names in Ulysses with relevant text extracts on a chapter by chapter basis
>python map-ml.py
output: new_uplaces.json

Produce a file that geocodes the place names on a chapter by chapter basis
>python map-geo.py
output: geo_uplaces.json

Plot these place names on an interactive map with folium
>python map-plot.py
output: map_plot.html
