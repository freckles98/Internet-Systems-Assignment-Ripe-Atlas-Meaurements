from datetime import datetime
from typing import Protocol
from ripe.atlas.cousteau import AtlasStream
from ripe.atlas.sagan import PingResult
from datetime import datetime
from ripe.atlas.cousteau import AtlasResultsRequest
import time
from ripe.atlas.sagan import Result
from ripe.atlas.sagan import PingResult, Result, TracerouteResult
import json
import json

from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)

ATLAS_API_KEY = "c32fa4b0-c010-4c0d-96e2-4a8a1ac1fa3f"

ping = Ping(af=4, target="137.158.154.230", description="testing new wrapper")

traceroute = Traceroute(
    af=4,
    target="41.63.1.33",
    description="testing",
    protocol="ICMP",
)

source = AtlasSource(type="area", value="WW", requested=5)

atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    key=ATLAS_API_KEY,
    measurements=[ping],
    sources=[source],
    is_oneoff=True
)

(is_success, response) = atlas_request.create()
time.sleep(200)
kwargs = {
    "msm_id": 32875166,

    }

is_success, results = AtlasResultsRequest(**kwargs).create()
    
# f = "test.json"
# with open(f, "w") as outfile:
#     json.dump(results, outfile)
#     for result in results:
#         print(Result.get(result))
item_dict = json.loads(results)


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
    print(my_result.af)                   # 4 or 6
    print(my_result.total_hops)           # Int
    print(my_result.destination_address)  # An IP address string
    print(my_result.ip_path)
    print(my_result.size)
    print(my_result.destination_ip_responded)