import requests
import json

requests.packages.urllib3.disable_warnings()


def get_vm_ids():
    vm_ids = []
    with open ("vms.txt", 'r') as vms_file:
        vms = vms_file.readlines()

    for vm in vms:
        strvm = str(vm).replace("\n", "")
        url = f"https://172.16.20.103/api/v1/fabric/virtual-machines?display_name={strvm}"

        payload = {}
        headers = {
          'Authorization': 'Basic YWRtaW46QnBvdnRtZzEhQnBvdnRtZzEh'
        }

        response = requests.request("GET", url, headers=headers, data=json.dumps(payload), verify=False)
        to_json = response.json()
        results = to_json.get("results")
        vm_id = results[0].get("external_id")
        vm_ids.append(vm_id)

    return vm_ids


def add_tags(vm_ids):
    for vm_id in vm_ids:
        url = f"https://172.16.20.103/api/v1/fabric/virtual-machines?action=update_tags"
        payload = {
        "external_id": f"{vm_id}",
        "tags": [
            {"scope": "test", "tag": "test"},
            {"scope": "security", "tag": "test"}
            ]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic YWRtaW46QnBvdnRtZzEhQnBvdnRtZzEh'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
        print(response.status_code)

vm_ids = get_vm_ids()
add_tags(vm_ids)
