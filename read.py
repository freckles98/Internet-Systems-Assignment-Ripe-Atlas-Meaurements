import re
import requests
import pyasn
from datetime import datetime
from typing import Protocol
from ripe.atlas.cousteau import AtlasStream
from ripe.atlas.sagan import PingResult
from datetime import datetime
from ripe.atlas.cousteau import AtlasResultsRequest
import time
import json
from ripe.atlas.sagan import PingResult,  TracerouteResult
import json
import requests

import pycountry
import matplotlib.pyplot as plt

import warnings
import numpy as np
import pyasn

from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)

def traceroute_results(traceroute_arr, file):
    for trace in traceroute_arr:   
        for output in range(1,len(trace),4):

            kwargs = {
            "msm_id": trace[output+2],

            }
            
            is_success, results = AtlasResultsRequest(**kwargs).create()
            print(trace[output+2])
            print(results)
            for x in range(len(results)):
                my_result = TracerouteResult(results[x])
                
                ip_path = my_result.ip_path
                country_dict = []
                country_count = 0
                print(ip_path)
                for ip in ip_path:
                    location = get_city_country(ip[0])

                    if  location != None and location[0] not in country_dict:
                        country_dict.append(location[0])
                        country_count += 1
                
                if my_result.is_success==True:
                    success = "successful"
                else:
                    success = "unsuccessful"
                print(trace[output],trace[output+3],"Traceroute for",trace[output+1],": from", my_result.source_address,"to", my_result.destination_address,".Total hops:", my_result.total_hops, "between", country_count,"different countries. The traceroute was", success )
                file.write(str(trace[output])+" "+str(trace[output+3])+" Traceroute for "+str(trace[output+1])+": from "+ str(my_result.source_address)+" to "+ str(my_result.destination_address)+". Total hops: "+ str(my_result.total_hops)+" between "+ str(country_count)+" different countries. The traceroute was "+ str(success)+"\n")
                hop = 1
                for ip in ip_path:
                    
                    location = get_city_country(ip[0])
                    if ip[0] == None or location==None:
                        
                        print("Hop ",hop,": from IP address:",ip[0],"with ASN None located in None")
                        file.write("Hop "+str(hop)+": from IP address: "+str(ip[0])+" with ASN None located in None \n")
                    else:
                        
                        location = get_city_country(ip[0])
                        
                        
                        try:
                            print("Hop ", hop,": from IP address:",ip[0],"with ASN", asndb.lookup(ip[0])[0],"located in",location[0],"with an RTT of",results[output]['result'][hop-1]['result'][0]['rtt'])
                            file.write("Hop " +str(hop)+": from IP address: "+str(ip[0])+"with ASN"+ str(asndb.lookup(ip[0])[0])+"located in"+str(location[0])+" with an RTT of "+str(results[output]['results']['rtt'])+"\n")
                        except:
                            print("Hop ", hop,": from IP address:",ip[0],"with ASN", asndb.lookup(ip[0])[0],"located in",location[0],"with an RTT of unknown")
                            file.write("Hop " +str(hop)+": from IP address: "+str(ip[0])+"with ASN"+ str(asndb.lookup(ip[0])[0])+"located in"+str(location[0])+"with an RTT of unknown\n")
                    hop+=1

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

asndb = pyasn.pyasn('ipasn6_20151101.dat.gz') #build database to find ASN
ATLAS_API_KEY = "c32fa4b0-c010-4c0d-96e2-4a8a1ac1fa3f"
file = open("measurement.txt","r")
output = file.read()
final_output = [[""],[""],[""],[""],[""]]
arr = output
arr = re.split("\" ", arr)
# print(arr[0][0])
# text = output.split('\n')
print()
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
        

#for measurement in final_output:

f = open("myfile.txt", "x")

icmp = traceroute_results(final_output[1:], f)




