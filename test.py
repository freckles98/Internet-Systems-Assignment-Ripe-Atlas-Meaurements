from datetime import datetime
from typing import Protocol
from ripe.atlas.cousteau import AtlasStream
from ripe.atlas.sagan import PingResult
from datetime import datetime
from ripe.atlas.cousteau import AtlasResultsRequest
import time
import json
from ripe.atlas.sagan import PingResult, Result, TracerouteResult
import json
import requests
import geopy 
from aslookup import get_as_data
import xml.etree.ElementTree as ET
import pycountry

#import cartopy.crs as ccrs
#from cartopy.feature import OCEAN
import warnings
import numpy as np
import pyasn
from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)
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
    return result['country_name'], result['city'] 



ATLAS_API_KEY = "c32fa4b0-c010-4c0d-96e2-4a8a1ac1fa3f"

# ping = Ping(af=4, target="196.2.164.249", description="Durban")

traceroute = Traceroute(
    af=4,
    target="129.122.16.228",
    description="testing",
    protocol="ICMP",
)

source = AtlasSource(type = "asn", value = 24757, requested = 1)

atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    key=ATLAS_API_KEY,
    measurements=[traceroute],
    sources=[source],
    is_oneoff=True
)

(is_success, response) = atlas_request.create()
print(is_success)
print(response)
time.sleep(20)
kwargs = {
    "msm_id": response['measurements'][0],

    }

is_success, results = AtlasResultsRequest(**kwargs).create()

# f = "test.json"
# with open(f, "w") as outfile:
#     json.dump(results, outfile)
#     for result in results:
#         print(Result.get(result))
#item_dict = json.loads(results)
print("hello")
asndb = pyasn.pyasn('ipasn6_20151101.dat.gz')
print(len(results))
for x in range(len(results)):
    print(len(results))
    my_result = TracerouteResult( results[x])
    print("yoohooo, big summer blowout")
    print(results[x])
   

    #print("Ping for X: Number of packets sent: ",my_result.packets_sent, " Number of packets received: ",my_result.packets_received, " Average RTT: ",my_result.rtt_median )
    
#     # Ping
# print(my_result.packets_sent)  # Int
# print(my_result.rtt_median)    # Float, rounded to 3 decimal places
# print(my_result.rtt_average)   # Float, rounded to 3 decimal places

   # print(results[x]['result'][6]['result'][0]['rtt'])
    #print(get_city_country('8.8.8.8'))
    
    print(asndb.lookup('8.8.8.8'))
    print(results[x]['result'][4]['result'][0])#['icmpext']['obj'][0]['mpls'][0]['label'])
# Traceroute
    ip_path = my_result.ip_path
    country_dict = []
    country_count = 0
    for ip in ip_path:
        location = get_city_country(ip[0])

        if  location != None and location[0] not in country_dict:
            country_dict.append(location[0])
            country_count += 1
    
    if my_result.is_success==True:
        success = "successful"
    else:
        success = "unsuccessful"
    print("ICMP Traceroute for X: from", my_result.source_address,"to", my_result.destination_address,".Total hops: ", my_result.total_hops, "between", country_count,"different countries. The traceroute was", success )
           # Int
      # An IP address string
    #print(my_result.ip_path)
    
   
    
    
    hop = 1
    for ip in ip_path:
        
        location = get_city_country(ip[0])
        if ip[0] == None or location==None:
            
            print("Hop ",hop,": from IP address:",ip[0],"with ASN None located in None")
        else:
            
            location = get_city_country(ip[0])
            
         
            print("Hop ",hop,": from IP address:",ip[0],"with ASN",asndb.lookup(ip[0])[0],"located in",location[0],"with an RTT of",results[x]['result'][hop-1]['result'][0]['rtt'])
       
        hop+=1

