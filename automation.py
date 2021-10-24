from datetime import datetime
from typing import Protocol
from ripe.atlas.cousteau import AtlasStream
from ripe.atlas.sagan import PingResult
from datetime import datetime
from ripe.atlas.cousteau import AtlasResultsRequest
import time

from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)

african_countries = [["ZA", "University of Cape Town","137.158.255.129", "University of Pretoria", "137.215.6.94", "Rhodes University","146.231.242.44" ],
                    ["GH", "University of Ghana", "197.255.125.213", "University of Cape Coast", "156.38.96.0"],
                    ["ET", "Jimma University", "197.154.187.0" ],
                    ["KE", "University of Nairobi", "41.89.94.20", "Kenyatta University", "41.89.10.241"],
                    ["UG", "Makerere University", "196.43.135.170", "Uganda Christian University", "102.220.200.167"],
                    ["DZ", "Universite de Jijel","193.194.69.172"],
                    ["MA", "Université Ibn Zohr", "196.200.181.122", "Al Akhawayn University", "196.12.203.30"],
                    ["SD", "Sudan University of Science and Technology", "41.67.52.0"],
                    ["RW", "University of Rwanda", "41.222.245.0"],
                    ["TZ", "University of Dar es Salaam", "196.44.160.0"],
                    ["ZM", "University of Zambia", "41.63.1.33"],
                    ["ZW", "University of Zimbabwe", "196.4.80.0"],
                    ["MU", "University of Mauritius", "202.60.7.12"],
                    ["NA", "University of Namibia", "41.205.129.157", "Namibia University of Science and Technology", "196.216.167.71"]]

#TO DO
#read the file
#differnt trace routes
#fix egypt and nigeria
ATLAS_API_KEY = "c32fa4b0-c010-4c0d-96e2-4a8a1ac1fa3f"
ping_arr = []
icmp_arr = []
udp_arr = []
tcp_arr = []
commence_time = datetime.utcnow()
#repeat for ping and traceroutes
for location in range(2):

    for x in range(2):
        for country in african_countries:
            country_code = country[0]
            print(country_code)
            if x==0:
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
                    if location == 0:
                        type_area = "country"
                        location_measurement = "intra"
                    if location == 1:
                        country_code = "South-Central"
                        type_area = "area"
                        location_measurement = "inter"
                    
                    ping = Ping(af=4, target=university_ip, description=university_name)
                    probes = AtlasSource(type=type_area, value=country_code, requested=5)

                    traceroute = Traceroute(
                        af=4,
                        target=university_ip,
                        description=university_name,
                        protocol=measure_protocol,
                    )
                    
                    if x==0:
                        measure = ping
                        measure_type = "ping"
                    else:
            
                        measure = traceroute
                        measure_type = "traceroute"

                    atlas_request = AtlasCreateRequest(
                        start_time=datetime.utcnow(),
                        key=ATLAS_API_KEY,
                        measurements=[measure],
                        sources=[probes],
                        is_oneoff=True
                        
                    )
                    
                    (is_success, response) = atlas_request.create()
                    if is_success:
                        print(response['measurements'][0])
                        
                        if measure_type=="ping":
                            ping_arr.append(location_measurement) 
                            ping_arr.append(university_name) 
                            ping_arr.append(response['measurements'][0])
                        else:
                            if measure_protocol == "ICMP":
                                icmp_arr.append(location_measurement)
                                icmp_arr.append(university_name)
                                icmp_arr.append(response['measurements'][0])
                            if measure_protocol == "TCP":
                                tcp_arr.append(location_measurement)
                                tcp_arr.append(university_name )
                                tcp_arr.append(response['measurements'][0])
                            if measure_protocol == "UDP":
                                udp_arr.append(location_measurement)
                                udp_arr.append(university_name)
                                udp_arr.append(response['measurements'][0])


time.sleep(200)

for ping in range(0,len(ping_arr),3):

    kwargs = {
    "msm_id": ping_arr[ping+2],

    }

    is_success, results = AtlasResultsRequest(**kwargs).create()
    
    f = open("ping/"+ping_arr[ping]+"_ping"+"_"+ping_arr[ping+1]+".txt", "w")
    f.write(str(results))

    f.close()

for icmp in range(0,len(icmp_arr),3):

    kwargs = {
    "msm_id": icmp_arr[icmp+2],

    }

    is_success, results = AtlasResultsRequest(**kwargs).create()
    
    f = open("traceroute/"+icmp_arr[icmp]+"_icmp"+"_"+icmp_arr[icmp+1]+".txt", "w")
    f.write(str(results))

    f.close()

for udp in range(0,len(udp_arr),3):

    kwargs = {
    "msm_id": udp_arr[udp+2],

    }

    is_success, results = AtlasResultsRequest(**kwargs).create()
    
    f = open("traceroute/"+udp_arr[udp]+"_udp"+"_"+udp_arr[udp+1]+".txt", "w")
    f.write(str(results))

    f.close()
for tcp in range(0,len(tcp_arr),3):

    kwargs = {
    "msm_id": tcp_arr[tcp+2],

    }

    is_success, results = AtlasResultsRequest(**kwargs).create()
    
    f = open("traceroute/"+tcp_arr[tcp]+"_tcp"+"_"+tcp_arr[tcp+1]+".txt", "w")
    f.write(str(results))

    f.close()

    
