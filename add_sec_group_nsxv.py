
# This script recive a .txt file with security group names and create them in nsx-v environment.
# Written by Ishak Shahak at 3/12/19

import requests
import sys
import time

# Ignore from requests module warnings.
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# Open the text file and read it.
securityGroupNames = open('sg.txt', 'r')

# REST API calls.
url = "https://192.168.41.70/api/2.0/services/securitygroup/universalroot-0"
headers = {
    'Content-Type': "application/xml",
    'Authorization': "Basic YWRtaW46UG9vbDEyIzE=",
    'User-Agent': "PostmanRuntime/7.18.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "9e79be41-6df0-42dc-9c00-c21e6df32026,67c09a82-de33-45f7-8a9b-f2885c85c6b8",
    'Host': "192.168.41.70",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "612",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

for securityGroupName in securityGroupNames:
    payload = "<securitygroup>\r\n<name>" + securityGroupName + "</name>\r\n<extendedAttributes>\r\n<extendedAttribute>\r\n\t<name>localMembersOnly</name>\r\n\t<value>true</value>\r\n</extendedAttribute>\r\n</extendedAttributes>\r\n</securitygroup>\r\n\r\n"
    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    if str(response.status_code) == "201":
        time.sleep(1)
        print ("Security group " + securityGroupName + " added!!")
    
