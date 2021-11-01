    
    
    
    
    
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
import geopy 

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

def traceroute_results(traceroute_arr):
  
      for x in range(len(results)):
          my_result = TracerouteResult(results[x])
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
          print("Traceroute for from", my_result.source_address,"to", my_result.destination_address,".Total hops:", my_result.total_hops, "between", country_count,"different countries. The traceroute was", success )
          file.write(" Traceroute for : from "+ str(my_result.source_address)+" to "+ str(my_result.destination_address)+". Total hops: "+ str(my_result.total_hops)+" between "+ str(country_count)+" different countries. The traceroute was "+ str(success)+"\n")
          hop = 1
          for ip in ip_path:
              
              location = get_city_country(ip[0])
              if ip[0] == None or location==None:
                  
                  print("Hop ",hop,": from IP address:",ip[0],"with ASN None located in None")
                  file.write("Hop "+str(hop)+": from IP address: "+str(ip[0])+" with ASN None located in None \n")
              else:
                  
                  location = get_city_country(ip[0])
                  
                  try:
                      print("Hop ", hop,": from IP address:",ip[0],"with ASN", asndb.lookup(ip[0])[0],"located in",location[0],"with an RTT of",results[0]['result'][hop-1]['result']['rtt'])
                      file.write("Hop " +str(hop)+": from IP address: "+str(ip[0])+"with ASN"+ str(asndb.lookup(ip[0])[0])+"located in"+str(location[0])+"with an RTT of"+str(results[0]['result'][hop-1]['result'][0]['rtt'])+"\n")
                  except:
                      print("Hop ", hop,": from IP address:",ip[0],"with ASN", asndb.lookup(ip[0])[0],"located in",location[0],"with an RTT of unknown")
                      file.write("Hop " +str(hop)+": from IP address: "+str(ip[0])+"with ASN"+ str(asndb.lookup(ip[0])[0])+"located in"+str(location[0])+"with an RTT of unknown\n")
              hop+=1
asndb = pyasn.pyasn('ipasn6_20151101.dat.gz') #build database to find ASN
ATLAS_API_KEY = "c32fa4b0-c010-4c0d-96e2-4a8a1ac1fa3f"
kwargs = {
"msm_id":  33075856,

}

is_success, results = AtlasResultsRequest(**kwargs).create()
print(results[0]['result'][7]['result'][0]['rtt'])
traceroute_results(results)