import requests
import json

requests.packages.urllib3.disable_warnings()


def check_sg_exist():
    sg_names = []
    url = "https://172.16.20.103/api/v1/ns-groups"

    payload = {}
    headers = {
        'Authorization': 'Basic YWRtaW46QnBvdnRtZzEhQnBvdnRtZzEh'
    }

    response = requests.request("GET", url, headers=headers, data=payload,  verify=False)
    results = response.json().get("results")
    for x in range(0, len(results)):
        name = results[x].get("display_name")
        sg_names.append(name)
    print(sg_names)

check_sg_exist()