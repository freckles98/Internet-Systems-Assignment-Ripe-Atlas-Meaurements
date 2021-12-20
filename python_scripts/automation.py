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
#funtion to return the country and city from the ip address
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

def traceroute_results(traceroute_arr, method, file):
    for output in range(0,len(traceroute_arr),3):

        kwargs = {
        "msm_id": traceroute_arr[output+2],

        }
        is_success, results = AtlasResultsRequest(**kwargs).create()
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
            print(traceroute_arr[output],method,"Traceroute for",traceroute_arr[output+1],": from", my_result.source_address,"to", my_result.destination_address,".Total hops:", my_result.total_hops, "between", country_count,"different countries. The traceroute was", success )
            file.write(str(traceroute_arr[output])+" "+str(method)+" Traceroute for "+str(traceroute_arr[output+1])+": from "+ str(my_result.source_address)+" to "+ str(my_result.destination_address)+". Total hops: "+ str(my_result.total_hops)+" between "+ str(country_count)+" different countries. The traceroute was "+ str(success)+"\n")
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
                        file.write("Hop " +str(hop)+": from IP address: "+str(ip[0])+"with ASN"+ str(asndb.lookup(ip[0])[0])+"located in"+str(location[0])+"with an RTT of"+str(results[output]['result'][hop-1]['result'][0]['rtt'])+"\n")
                    except:
                        print("Hop ", hop,": from IP address:",ip[0],"with ASN", asndb.lookup(ip[0])[0],"located in",location[0],"with an RTT of unknown")
                        file.write("Hop " +str(hop)+": from IP address: "+str(ip[0])+"with ASN"+ str(asndb.lookup(ip[0])[0])+"located in"+str(location[0])+"with an RTT of unknown\n")
                hop+=1


asndb = pyasn.pyasn('ipasn6_20151101.dat.gz') #build database to find ASN

african_universities = [
                    ["ZA", "University of the Western Cape","154.0.173.19", "Durban University of Technology", "196.2.164.249", "Rhodes University","146.231.128.43" ],
                    ["GH", "University of Ghana", "197.255.125.213", "University of Cape Coast", "156.38.97.106","Kwame Nkrumah University of Science & Technology","129.122.16.228"],
                    ["KE", "University of Nairobi", "41.89.94.20", "Mount Kenya University", "208.109.41.232"],
                    ["UG", "Ndejje University", "216.104.200.12", "Uganda Christian University", "102.220.200.167"],
                    ["DZ", "Universite de Jijel","193.194.69.172"],
                    ["MA", "Université Ibn Zohr", "196.200.181.122", "University of Hassan II Casablanca", "196.200.165.54"],
                    ["SD", "University of Medical Sciences and Technology (UMST)", "197.251.68.25"],
                    ["TZ", "The Open University of Tanzania", "196.216.247.18", "Sokoine University of Agriculture", "41.73.194.141"],
                    ["ZM", "Mulungushi University", "41.63.16.3","University of Lusaka", "41.63.7.238"],
                    ["NG", "Obafemi Awolowo University", "196.27.128.12"],
                    ["NA", "University of Namibia", "41.205.129.157", "Namibia University of Science and Technology", "196.216.167.71"]]

#personal API from Ripe Atlas
ATLAS_API_KEY = "c32fa4b0-c010-4c0d-96e2-4a8a1ac1fa3f"

ping_arr = []
icmp_arr = []
udp_arr = []
tcp_arr = []
commence_time = datetime.utcnow()

#two loops for intra and inter lookups
for location in range(2):
    #repeat for ping and traceroutes
   for ping_variable in range(2):
        
        for country in african_universities:
            country_code = country[0]
            print(country_code)
            if ping_variable==0:
                repetitions = 1

            else:
                repetitions = 3
            

            #repeat for traceroute different protocols   
            for repeat in range(repetitions):
                if repeat == 0:
                    measure_protocol = "ICMP"
                if repeat == 1:
                    measure_protocol = "TCP"
                if repeat == 2:
                    measure_protocol = "UDP"
                for university in range(1,len(country)-1,2):
                    print(country[university])
                    university_name = country[university]
                    university_ip =country[university+1]
                    if location == 1:
                        type_area = "country"
                        location_measurement = "Intra"
                        probes = [AtlasSource(type="country", value=country_code, requested=5)]
                    else:
                        #assigned specific probes to analyse inter networks
                        type_area = "area"
                        location_measurement = "Inter"
                        namibiaprobe = AtlasSource(type = "country", value = "NA", requested = 1)
                        ethiopiaprobe = AtlasSource(type = "country", value = "ET", requested = 1)
                        senegalprobe = AtlasSource(type = "country", value = "SN", requested = 1)
                        gabonprobe = AtlasSource(type = "country", value = "GA", requested = 1)
                        tusiniaprobe = AtlasSource(type = "country", value =  "TN", requested = 1)
                        probes = [namibiaprobe, ethiopiaprobe, senegalprobe, gabonprobe,tusiniaprobe]
                    
                    ping = Ping(af=4, target=university_ip, description=university_name)
                    
                    

                    traceroute = Traceroute(
                        af=4,
                        target=university_ip,
                        description=university_name,
                        protocol=measure_protocol,
                    )
                    
                    if ping_variable==0:
                        measure = ping
                        measure_type = "ping"

                    else:
                        measure = traceroute
                        measure_type = "traceroute"

                    #create the request
                    atlas_request = AtlasCreateRequest(
                        start_time=datetime.utcnow(),
                        key=ATLAS_API_KEY,
                        measurements=[measure],
                        sources=probes,
                        is_oneoff=True
                        
                    )
                    
                    (is_success, response) = atlas_request.create()
                    

                    if is_success:
                        print(response['measurements'][0])
                        
                        if measure_type=="ping":
                            ping_arr.append(location_measurement) 
                            ping_arr.append(university_name) 
                            ping_arr.append(response['measurements'][0])
                            ping_arr.append(measure_protocol)
                        else:
                            if measure_protocol == "ICMP":
                                icmp_arr.append(location_measurement)
                                icmp_arr.append(university_name)
                                icmp_arr.append(response['measurements'][0])
                                icmp_arr.append(measure_protocol)
                            if measure_protocol == "TCP":
                                tcp_arr.append(location_measurement)
                                tcp_arr.append(university_name )
                                tcp_arr.append(response['measurements'][0])
                                tcp_arr.append(measure_protocol)
                            if measure_protocol == "UDP":
                                udp_arr.append(location_measurement)
                                udp_arr.append(university_name)
                                udp_arr.append(response['measurements'][0])
                                udp_arr.append(measure_protocol)

file = open("measurement.txt", "x")
print(ping_arr)
print(icmp_arr)
print(tcp_arr)
print(udp_arr)
file.write(str(ping_arr)+"\n")
file.write(str(icmp_arr)+"\n")
file.write(str(tcp_arr)+"\n")
file.write(str(ping_arr)+"\n")
file.close()





