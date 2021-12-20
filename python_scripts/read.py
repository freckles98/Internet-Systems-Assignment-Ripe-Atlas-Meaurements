import re
import requests
import pyasn
import statistics
from datetime import datetime
from typing import Protocol
from ripe.atlas.cousteau import AtlasStream
from ripe.atlas.sagan import PingResult
from datetime import datetime
from ripe.atlas.cousteau import AtlasResultsRequest
import time
import json
from ripe.atlas.sagan import PingResult,  TracerouteResult, Result
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


def ping_results(ping_arr, file, dict):
    #todo
    # dict = country: [rtt,rtt,rtt,rtt]
    # 
    
    for ping in range(1,len(ping_arr),4):
        
        kwargs = {
        "msm_id": ping_arr[ping+2],

        }

        is_success, results = AtlasResultsRequest(**kwargs).create()
        median_list = []
        count = 0
        for x in range(len(results)):
            
            my_result = PingResult(results[x])
            try:
                if not isinstance(my_result.rtt_median, str):
                                median_list.append( int(my_result.rtt_median))
                                count +=1
                                
                print(ping_arr[ping],"Ping for "+ping_arr[ping+1],": Number of packets sent: ",my_result.packets_sent, "Number of packets received:", my_result.packets_received , "Average RTT: ", my_result.rtt_median )
                f.write(str(ping_arr[ping])+" Ping for "+str(ping_arr[ping+1])+": Number of packets sent: "+str(my_result.packets_sent)+ " Number of packets received: "+ str(my_result.packets_received)+ " Average RTT: "+ str(my_result.rtt_median)+".\n")
            except:
                print(ping_arr[ping],"Ping for "+ping_arr[ping+1],"failed")
                file.write(str(ping_arr[ping])+" Ping for "+str(ping_arr[ping+1])+" failed.\n")
            
        median = np.median(median_list)
        print("Median ping rtt:",median, count)
        file.write("Median ping rtt: "+str(median)+"\n")
        
        key = ping_arr[ping]+" "+ping_arr[ping+1]
       
        if key in dict.keys():
            
            print(key, dict[key])
            print(type(dict[key]))
            arr = dict[key] + [median]
            
            print(arr)
            dict[key] = arr
        else:
            arr = [median]
            print(arr)
            
            dict.update({key:arr})
        print(dict)

    print("===========================================================================================================================\n")
    file.write("\n===========================================================================================================================\n")
    return dict


def traceroute_results(traceroute_arr, file,  icmp_dict, tcp_dict, asndb):
    #icmpdict country: [icmp rtt, icmp hops, icmp inter hops]
    # tcp dict country: [rtt, hops, inter hops]
    for trace in traceroute_arr:   
        for output in range(1,len(trace),4):

            kwargs = {
            "msm_id": trace[output+2],

            }
            
            is_success, results = AtlasResultsRequest(**kwargs).create()
            median_list = []
            inter_country_hops = 0
            number_of_hops = 0
            count = 0
            for x in range(len(results)):
                my_result = TracerouteResult(results[x])
                ip_path = my_result.ip_path
                country_dict = []
                country_count = 0
                
                if my_result.is_success==True:
                    success = "successful"
                else:
                    success = "unsuccessful"
                #print("\n",trace[output],trace[output+3],"Traceroute for",trace[output+1],": from", my_result.source_address,"to", my_result.destination_address,".Total hops:", my_result.total_hops, ". The traceroute was", success, "with a last median rtt of ",my_result.last_median_rtt)
                file.write("\n\n"+str(trace[output])+" "+str(trace[output+3])+" Traceroute for "+str(trace[output+1])+": from "+ str(my_result.source_address)+" to "+ str(my_result.destination_address)+". Total hops: "+ str(my_result.total_hops)+". The traceroute was "+ str(success)+" with a last median rtt of "+str(my_result.last_median_rtt)+"\n")
                
                
                number_of_hops += my_result.total_hops
                count += 1
                if not ((my_result.last_median_rtt is None) or isinstance(my_result.last_median_rtt, str)):
                                median_list.append( int(my_result.last_median_rtt))
                                

                hop = 1
                
                for ip in ip_path:
                    
                    location = get_city_country(ip[0])

                   

                    if  location != None and location[0] not in country_dict:
                        country_dict.append(location[0])
                        country_count += 1
                
                
                    if ip[0] == None or location==None:
                        
                        #print("Hop ",hop,": from IP address:",ip[0],"with ASN None located in None")
                        file.write("Hop "+str(hop)+": from IP address: "+str(ip[0])+" with ASN None located in None \n")
                    else:
                        
                        try:
                            #print("Hop ", hop,": from IP address:",ip[0],"with ASN", asndb.lookup(ip[0])[0],"located in",location[0],"with an RTT of",my_result.hops[hop-1].median_rtt)
                            file.write("Hop " +str(hop)+": from IP address: "+str(ip[0])+" with ASN "+ str(asndb.lookup(ip[0])[0])+" located in "+str(location[0])+" with an RTT of "+str(my_result.hops[hop-1].median_rtt)+"\n")
            
                        except:
                            try:
                                #print("Hop ", hop,": from IP address:",ip[0],"with ASN", asndb.lookup(ip[0])[0],"located in",location[0],"with an RTT of None")
                                file.write("Hop " +str(hop)+": from IP address: "+str(ip[0])+" with ASN "+ str(asndb.lookup(ip[0])[0])+" located in "+str(location[0])+" with an RTT of None\n")
                            except:
                                #print("Hop ", hop,": from IP address:",ip[0],"with ASN", None,"located in",None,"with an RTT of None")
                                file.write("Hop " +str(hop)+": from IP address: "+str(ip[0])+" with ASN "+ str(None)+" located in "+str(None)+" with an RTT of None\n")
                    hop+=1
                inter_country_hops += country_count
                file.write("Number of Inter Country hops: "+str(country_count)+"\n")
                
                #print("Number of Inter Country hops: ", country_count)
            median = np.median(median_list)
            average_no_hops = 0
            average_no_inter_hops = 0
            if count > 0:
                average_no_hops = number_of_hops/count
                average_no_inter_hops = inter_country_hops/count
            print("Median traceroute rtt:",median,"Average number of hops",average_no_hops, "Average number of intercountry hops:", average_no_inter_hops)
            file.write("Median traceroute rtt: "+str(median)+" Average number of hops "+str(average_no_hops)+ " Average number of intercountry hops: "+ str(average_no_inter_hops)+"\n")
            
            
            appending = [median]+ [average_no_hops] + [average_no_inter_hops]
            if trace[output+3]=="ICMP":
                key = trace[output]+" "+trace[output+1]
       
                if key in icmp_dict:
                    
                    arr = icmp_dict[key]+appending
                    icmp_dict.update({key: arr})
                else:
                    
                    
                    icmp_dict.update({key:appending})
                print(icmp_dict)
               
            if trace[output+3] == "TCP":
                key = trace[output]+" "+trace[output+1]
       
                if key in tcp_dict:
                   
                    arr = tcp_dict[key] +appending
                    tcp_dict.update({key: arr})
                else:
                    arr = appending
                    
                    tcp_dict.update({key:arr})
                print(tcp_dict)
    return icmp_dict, tcp_dict


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

def write_to_file(dict):
    for key in dict:
        total_rtt = 0
        total_hops = 0
        total_inter_hops = 0
        count = 0
        arr = dict.get(key)
        for index in range(0,len(arr),3):
            total_rtt+= arr[index]
            total_hops += arr[index+1]
            total_inter_hops += arr[index+2]
            count+=1
        if count > 0:
            average_rtt = total_rtt/count
            average_hops = total_hops/count
            average_inter_hops = total_inter_hops/count
            average_file.write(str(key)+" Traceroute with a total average RTT of : "+str(average_rtt)+" Average number of hops: "+str(average_hops)+ " Average number of inter hops: "+str(average_inter_hops)+"\n")
        else:
            average_file.write(str(key)+" Traceroute failed.\n")



ping_dict = {}
icmp_dict = {}
tcp_dict = {}


file_1 = "measurement 29 Oct 10am.txt"
file_2 = "measurement 29 Oct 10pm.txt"
file_3 = "measurement 29 Oct 2pm.txt"
files = [file_1,file_2, file_3]

asndb = pyasn.pyasn('ipasn6_20151101.dat.gz') #build database to find ASN
ATLAS_API_KEY = "c32fa4b0-c010-4c0d-96e2-4a8a1ac1fa3f"
f = open("myfile.txt", "x")

average_file = open("final.txt", "x")

for file in files:
    final_output = read_measurement(file)
    #ping_dict = ping_results(final_output[0],f, ping_dict)
    icmp_dict, tcp_dict = traceroute_results(final_output[0:2], f,  icmp_dict, tcp_dict, asndb)


#dictionary format = {country:[ping rtt, icmp rtt, icmp hops, icmp inter hops, tcp rtt tcp hops, tcp inter hops]}

for key in ping_dict:
    total_rtt = 0
    count = 0
    arr = ping_dict.get(key)
    for rtt in arr:
        total_rtt+= rtt
        count+=1
    if count > 0:
        average = total_rtt/count
        print(average, total_rtt,count )
        average_file.write(str(key)+" Ping with a total average RTT of : "+str(average)+"\n")
    else:
        average_file.write(str(key)+" Ping RTT failed.\n")

write_to_file(icmp_dict)
write_to_file(tcp_dict)
    
    






