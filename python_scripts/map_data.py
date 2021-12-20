# %%
from ripe.atlas.sagan import PingResult, Result, TracerouteResult
import json
import requests
import geopy 
import pycountry
import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# from cartopy.feature import OCEAN
import re
import warnings
import numpy as np
from mpl_toolkits.basemap import Basemap
import geopandas
from shapely.geometry import Point, Polygon, LineString
import pandas as pd
import pyasn
from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)
from ripe.atlas.cousteau import AtlasResultsRequest


def get_city_country(ip):
    if ip ==None:
        return None
    request_url = 'https://api.freegeoip.app/json/'+str(ip)+'?apikey=7ffce290-3820-11ec-8b11-3d3e1977f86e'#+ str(ip)
    response = requests.get(request_url)
    if response.status_code != 200:
        
        return None
    result  = response.json()
   
    
    if result.get('city') == None:
        return None
    return result['country_name'], result['city'], result['latitude'], result['longitude']



def plot(geometry, colour):
    fig, ax = plt.subplots(figsize=(20,11))
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world.plot(ax = ax, edgecolor ='k')
    
    
   
    crs={'init':'epsg:4326'}
    geodata = geopandas.GeoDataFrame(crs=crs, geometry=geometry)
    geodata['colour'] = colour
    
    geodata.plot(ax=ax, markersize=5, color = geodata.colour)
   
    fig.suptitle('Intra Country Traceroutes', fontsize=20)
    ax.set_xlabel('Longitude', fontsize=10)
    ax.set_ylabel('Latitude', fontsize='medium')

# filename = "traceroute/intra_tcp_Université Ibn Zohr.json"
# results = open(filename).read()
# item_dict = json.loads(results)

# base = world.plot(color='white', edgecolor='black')

# cities.plot(ax=base, marker='o', color='red', markersize=5);

# for x in range(len(item_dict)):
#     my_result = TracerouteResult( item_dict[x])

asndb = pyasn.pyasn('ipasn6_20151101.dat.gz') #build database to find ASN
ATLAS_API_KEY = "c32fa4b0-c010-4c0d-96e2-4a8a1ac1fa3f"

def plot_one_measurement():

    kwargs = {
    "msm_id":  33075829,

    }
    is_success, results = AtlasResultsRequest(**kwargs).create()
    geometry = []
    colour = []
    geometry_points = []
    geometry_lines = []
    colour_points = []
    colour_lines = []
    for x in range(len(results)):
        
        my_result = TracerouteResult( results[x])
        
        print(results[x])
        ip_path = my_result.ip_path
        country_dict = []
        country_count = 0
        
        

        for ip in ip_path:
            location = get_city_country(ip[0])
            

            if  location != None and not (location[2]==0 and location[3]==0):
                country_dict.append(location[0])
                country_count += 1
                print(location[0], location[3],location[2])
                geometry_points.append(Point(location[3],location[2]))
                if x == 0:
                    colour_points.append('r')
                    print("red")
                elif x ==1:
                    colour_points.append('#00FF00')
                    print("blue")
                elif x == 2:
                    colour_points.append('#FFFF00')
                    print("green")
                elif x==3:
                    colour_points.append('#FFC0CB')
                    print("sepia")
                else:
                    colour_points.append('#000000')
                    print("other")
            
                if len(geometry_points) > 1:

                    geometry_lines.append(LineString([geometry_points[-2], Point(location[3],location[2])]))
                    if x == 0:
                        colour_lines.append('#00FF00')
                    elif x ==1:
                        colour_lines.append('r')
                    elif x == 2:
                        colour_lines.append('b')
                    elif x==3:
                        colour_lines.append('g')
                    else:
                        colour_lines.append('#000000')
    
    
    geometry = geometry_points + geometry_lines
    colour = colour_points + colour_lines
    print(colour)

    plot(geometry, colour)


def read_measurement(measurement_file):
    file = open(measurement_file,"r")
    output = file.read()
    final_output = [[""],[""],[""],[""],[""]]
    arr = output
    arr = re.split("\" ", arr)
    # print(arr[0][0])
    # text = output.split('\n')

    text = output.split(",")

    output_index = 0


    characters_to_remove = "[]'"
    for x in text:
        
        stripped = x.strip("\' ")
        
        bracket_exists = "]" in stripped
        
        if bracket_exists:
            new_string = stripped
            for character in characters_to_remove:
                new_string = new_string.replace(character, "")
            
            
            strip = new_string.split("\n")
            
            final_output[output_index].append(strip[0])
            output_index += 1
            final_output[output_index].append(strip[1])
            
        else:
            stripped = x.strip("\'[] ")
        
            final_output[output_index].append(stripped)
    return final_output

def plot_multiple_measurements():
    file = "measurement for mapping.txt"
    dict = {0:"#e6194B", 1:'#3cb44b', 2: '#ffe119', 3:'#4363d8', 4:'#f58231', 5:'#911eb4', 6:'#42d4f4', 7:'#f032e6', 8:'#bfef45', 9:'#fabed4', 10:'#469990', 11:'#dcbeff', 12:'#9A6324', 13:'#fffac8', 14:'#800000', 15:'#aaffc3', 16:'#808000', 17:'#ffd8b1', 18:'#000075', 19:'#a9a9a9', 20:'#ffffff', 21:'#000000'}
    traceroute_arr = read_measurement(file)
    geometry = []
    colour = []
    geometry_points = []
    geometry_lines = []
    colour_points = []
    colour_lines = []
    
    for trace in traceroute_arr[1:3]: 
        for output in range(1,len(trace),4): 
            kwargs = {
            "msm_id":  trace[output+2],

            }
            is_success, results = AtlasResultsRequest(**kwargs).create()
           
            #for x in range(len(results)):
            if trace[output] == "Intra" and not trace[output+1]=='Mount Kenya University':
                
                my_result = TracerouteResult( results[0])
                
                
                ip_path = my_result.ip_path
                country_dict = []
                country_count = 0
                
                

                for ip in ip_path:
                    location = get_city_country(ip[0])
                    

                    if  location != None and not (location[2]==0 and location[3]==0):
                        country_dict.append(location[0])
                        country_count += 1
                        print(location[0],location[1])
                        geometry_points.append(Point(location[3],location[2]))
                        key = (output-1-84)/4
                        
                        colour_points.append(dict[key])
                       
                        if len(geometry_points) > 1:

                            geometry_lines.append(LineString([geometry_points[-2], Point(location[3],location[2])]))
                            key = (output-1-84)/4
                        
                            colour_points.append(dict[key])
            
            
            geometry = geometry_points + geometry_lines
            colour = colour_points + colour_lines
       

    plot(geometry, colour)

plot_multiple_measurements()

# %%
