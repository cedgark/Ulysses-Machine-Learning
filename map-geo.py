# importing geopy library
from geopy.geocoders import Nominatim

# for calculating the distance between locations
from geopy.distance import geodesic

import json

# Import statistics Library
import statistics

def load_data(file): #load json data
    with open(file,'r') as g:
        places = json.load(g) #get GPEs. This is a file containing place names and their extracts
        return places

def save_data(file,data):
    with open(file,'w') as f:
        json.dump(data,f,indent=4)

ie_data = load_data('new_uplaces.json') # load gpes' with extracts

new_ie_data = {} # gpes' with extracts and coordinates
#print(ie_data)

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")

# entering the main location name
loc1 = loc.geocode("Dublin")

# printing address
print(loc1.address)

# printing latitude and longitude
print("Latitude = ", loc1.latitude, "\n")
print("Longitude = ", loc1.longitude)

for chapter_num in ie_data: # geocode each place name on a chapter by chapter basis
    results = []
    chapter_hits = ie_data[chapter_num]
    for hit in chapter_hits:
        place_name = hit[0]
        place_text = hit[1]

        try:
            print('Chapter number: ',chapter_num)
            print('place name: ',place_name)
            loc2 = loc.geocode(place_name + ' '+ 'Dublin 1904',country_codes ='IE') # Limit results to Ireland, Dublin 1904 (The date the events of Ulysses takes place)

            print(loc2.address)

            loca = (loc1.latitude, loc1.longitude)
            locb = (loc2.latitude,loc2.longitude)

            # calculate the distance between location 1 and location 2

            place_dist = geodesic(loca,locb).miles

            if place_dist < 22: # if place distance is within Dublin, add the coordinates
                results.append([place_name, place_text,locb])

        except Exception as e:
            print('No result')
            pass

    new_ie_data[chapter_num] = results # store gpe,extract and coordinates
    print(new_ie_data)
    save_data('geo_uplaces.json',new_ie_data)
