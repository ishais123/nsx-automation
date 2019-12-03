# This script recive a .txt file with security group object ID's and delete them in nsx-v environment.
# To get all security groups ID's you can use REST API call below: GET https://192.168.41.70/api/2.0/services/securitygroup/scope/universalroot-0
# If you use global security group (not universial object in cross vCnter NSX, use "globalroot-0" instead of "universialroot-0".
# Written by Ishak Shahak at 3/12/19.

import requests
import sys
import time

# Ignore from requests module warnings.
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# Open the text file and read it.
idsFile = open('sg_id.txt', 'r')


# REST API calls.
payload = ""
headers = {
    'Authorization': "Basic YWRtaW46UG9vbDEyIzE=",
    'User-Agent': "PostmanRuntime/7.18.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "de051c58-b242-431c-9458-7042a324f016,38952351-9012-43b9-88c1-d79c7468ed9a",
    'Host': "192.168.41.70",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "0",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }
    
for id in idsFile:
    id = id.replace("\n", "")
    url = "https://192.168.41.70/api/2.0/services/securitygroup/" + id
    response = requests.request("DELETE", url, data=payload, headers=headers, verify=False)
    if str(response.status_code) == "200" or str(response.status_code) == "204":
        time.sleep(1)
        print ("Security group with ID: " + id + " deleted!!")
