import json

import folium

def load_data(file): #load json data
    with open(file,'r') as g:
        places = json.load(g) #get GPEs. This is a file containing place names and their extracts
        return places

ie_data = load_data('geo_uplaces.json') # load gpes' with extracts and coordinates

map = folium.Map(location=[53.3498006,-6.2602964],zoom_start=13) # create base map of Dublin

map.add_child(folium.Marker(location=[53.3498006,-6.2602964],popup='Dublin'))

for chapter_num in ie_data: # map each place name on a chapter by chapter basis based on coordinates
    #results = []
    chapter_hits = ie_data[chapter_num]
    for hit in chapter_hits:
        place_name = hit[0]
        place_text = hit[1]
        place_long = hit[2][0]
        place_lat = hit[2][1]
        map.add_child(folium.Marker(location=[place_long,place_lat],popup=place_name))






map.save('map_plot.html')
