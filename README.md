# Ulysses-Machine-Learning
Uses machine learning to map all locations in the novel Ulysses by James Joyce using Spacy

Produce a file containing all place names in Ulysses with relevant text extracts on a chapter by chapter basis
>python map-ml.py
output: new_uplaces.json

Produce a file that geocodes the place names on a chapter by chapter basis
>python map-geo.py
output: geo_uplaces.json

Plot these place names on an interactive map with folium
>python map-plot.py
output: map_plot.html
