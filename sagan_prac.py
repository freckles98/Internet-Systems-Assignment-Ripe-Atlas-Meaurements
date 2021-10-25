from ripe.atlas.sagan import PingResult, Result, TracerouteResult
import json
import requests
import geopy 
import Nominatim

def get(ip):
    endpoint = f'https://ipinfo.io/{ip}/json'
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'
        exit()

    data = response.json()
    print(data)
    if data.get('city') == None:
        return None
    return data['city']

def plot_city(adress):
    address=adress
    geolocator =  Nominatim(user_agent="Your_Name")
    location = geolocator.geocode(address)
    print(location.address)
    print((location.latitude, location.longitude))

filename = "traceroute/intra_tcp_Université Ibn Zohr.json"
results = open(filename).read()
item_dict = json.loads(results)

base = world.plot(color='white', edgecolor='black')

cities.plot(ax=base, marker='o', color='red', markersize=5);

for x in range(len(item_dict)):
    my_result = TracerouteResult( item_dict[x])

#     print(my_result)
#     print(my_result.af)
#     print(my_result.rtt_median)

#     # Ping
# print(my_result.packets_sent)  # Int
# print(my_result.rtt_median)    # Float, rounded to 3 decimal places
# print(my_result.rtt_average)   # Float, rounded to 3 decimal places

   
# Traceroute
    ip_path = my_result.ip_path
    print(my_result.af)                   # 4 or 6
    print(my_result.total_hops)           # Int
    print(my_result.destination_address)  # An IP address string
    print(my_result.ip_path)
    print(my_result.total_hops)
    print(my_result.destination_ip_responded)
    my_country = get("196.74.34.70")

    print(my_country)
    for ip in ip_path:
        print(get(ip[0]))
# # DNS
# my_result.responses                        # A list of Response objects
# my_result.responses[0].response_time       # Float, rounded to 3 decimal places
# my_result.responses[0].headers             # A list of Header objects
# my_result.responses[0].headers[0].nscount  # The NSCOUNT value for the first header
# my_result.responses[0].questions           # A list of Question objects
# my_result.responses[0].questions[0].type   # The TYPE value for the first question
# my_result.responses[0].abuf                # The raw, unparsed abuf string

# # SSL Certificates
# my_result.af                        # 4 or 6
# my_result.certificates              # A list of Certificate objects
# my_result.certificates[0].checksum  # The checksum for the first certificate

# # HTTP
# my_result.af                      # 4 or 6
# my_result.uri                     # A URL string
# my_result.responses               # A list of Response objects
# my_result.responses[0].body_size  # The size of the body of the first response

# # NTP
# my_result.af                          # 4 or 6
# my_result.stratum                     # Statum id
# my_result.version                     # Version number
# my_result.packets[0].final_timestamp  # A float representing a high-precision NTP timestamp
# my_result.rtt_median          





