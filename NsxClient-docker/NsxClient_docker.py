# This Client receive CSV file (mapping.csv) and TXT file (vms.txt)
# The files have to be in the same directory as the script.
# Files should contain the tags and scopes information for the security group.


"""
Example :
env --> prod
app --> ishaiApp
os --> linux
The Client will create a securiy group named "custom-prod-ishaiApp-linux" with 3 tag crateria (env: prod, app: ishaiApp and os: linux)
"""
# Writen by Ishai Shahak at 12/4/19
# Updated by Ishai Shahak at 22/01/20

import requests
import json
import time
import argparse
import pandas
from colorama import init
from termcolor import colored
import pyfiglet

requests.packages.urllib3.disable_warnings()  # Ignore from requests module warnings

MAPPING_FILE = '/map/mapping.csv'

ADD_GROUP_URI = "api/v1/ns-groups"
CHECK_SG_EXIST = "api/v1/ns-groups"
AUTHORIZATION_URI = "api/session/create"
ADD_TAGS_URI = "api/v1/fabric/virtual-machines?action=update_tags"

init() # colors for prints (Mandatory!!)
font = pyfiglet.Figlet(font='standard')
welcome_message = font.renderText("Hello to NsxClient!!")
print(welcome_message)


class NsxClient:

    def __init__(self, nsx_manager):
        self.session = requests.Session()
        self.nsx_manager = nsx_manager
        self.mapping = pandas.read_csv(MAPPING_FILE, sep=',')

    def authorize(self, username, password):
        self.username = username
        self.password = password
        url = f"https://{self.nsx_manager}/{AUTHORIZATION_URI}"
        data = {"j_username": self.username, "j_password": self.password}
        response = self.session.request("POST", url, data=data, verify=False)
        self.xsrf_token = response.headers['X-XSRF-TOKEN']
        self.headers = {
            'Content-Type': "application/json",
            'User-Agent': "PostmanRuntime/7.19.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': self.nsx_manager,
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "573",
            'Connection': "keep-alive",
            'cache-control': "no-cache",
            'X-XSRF-TOKEN': self.xsrf_token
        }

    def get_vm_ids(self):
        vm_ids = []
        vms = self.mapping['VM']
        for vm in vms:
            str_vm = str(vm).replace("\n", "")
            url = f"https://{self.nsx_manager}/api/v1/fabric/virtual-machines?display_name={str_vm}"
            payload = {}
            response = self.session.request("GET", url, headers=self.headers, data=json.dumps(payload), verify=False)
            to_json = response.json()
            results = to_json.get("results")
            vm_id = results[0].get("external_id")
            vm_ids.append(vm_id)

        return vm_ids

    def check_sg_exist(self, sg_name):
        sg_names = []
        url = f"https://{self.nsx_manager}/{CHECK_SG_EXIST}"
        payload = {}
        response = self.session.request("GET", url, headers=self.headers, data=json.dumps(payload), verify=False)
        results = response.json().get("results")
        for x in range(0, len(results)-1):
            name = results[x].get("display_name")
            sg_names.append(name)
        if sg_name in sg_names:
            return True
        else:
            return False

    def add_security_group(self):
        count = 0
        print(colored("Starting to add security groups...", 'yellow', attrs=['bold']))
        print("-----------")
        time.sleep(2)
        # REST API calls
        url = f"https://{self.nsx_manager}/{ADD_GROUP_URI}"

        for x in range(0, len(self.mapping['VM'])):
            env_tag = self.mapping['ENV'][x]
            app_tag = self.mapping['APP'][x]
            os_tag = self.mapping['OS'][x]
            display_name = f"custom-{env_tag}-{app_tag}-{os_tag}"
            if not self.check_sg_exist(display_name):
                payload = {
                    "display_name": display_name,
                    "membership_criteria": [
                        {
                            "resource_type": "NSGroupComplexExpression",
                            "expressions": [
                                {
                                    "resource_type": "NSGroupTagExpression",
                                    "target_type": "VirtualMachine",
                                    "scope": "env",
                                    "tag": env_tag
                                },
                                {
                                    "resource_type": "NSGroupTagExpression",
                                    "target_type": "VirtualMachine",
                                    "scope": "app",
                                    "tag": app_tag
                                },
                                {
                                    "resource_type": "NSGroupTagExpression",
                                    "target_type": "VirtualMachine",
                                    "scope": "os",
                                    "tag": os_tag
                                }
                            ]
                        }
                    ]
                }
                response = self.session.request("POST", url, data=json.dumps(payload), headers=self.headers, verify=False)

                if str(response.status_code) == "201":
                    count = count + 1
                    time.sleep(1)
                    print(f"Security group {display_name} added.")
                else:
                    print(response.text)
            else:
                print(colored(f"Security group {display_name} already exists", 'red'))
                continue
        if count == len(self.mapping['VM']):
            time.sleep(2)
            print("-----------")
            print(colored("\nAll Security groups added.", 'green', attrs=['bold']))

    def add_tags(self):
        vm_ids = self.get_vm_ids()
        count = 0
        print(colored("\nStarting to add security tags...", 'yellow', attrs=['bold']))
        print("-----------")
        time.sleep(2)

        for x in range(0, len(self.mapping['VM'])):
            url = f"https://{self.nsx_manager}/{ADD_TAGS_URI}"

            payload = {
                "external_id": f"{vm_ids[x]}",
                "tags": [
                    {"scope": "env", "tag": self.mapping['ENV'][x]},
                    {"scope": "app", "tag": self.mapping['APP'][x]},
                    {"scope": "os", "tag": self.mapping['OS'][x]}
                ]
            }
            response = self.session.request("POST", url, headers=self.headers, data=json.dumps(payload), verify=False)
            if str(response.status_code) == "204":
                count = count + 1
                print(f"Tags added to VM {self.mapping['VM'][x]}")
        if count == len(self.mapping['VM']):
            time.sleep(2)
            print("-----------")
            print(colored("All Tags added.", 'green', attrs=['bold']))

#
# def parse_args():
#     parser = argparse.ArgumentParser(description='Enter IP, Username and Password of NSX Node.')
#     parser.add_argument("-i", "--ip", help="IP address of the NSX Manager.")
#     parser.add_argument("-u", "--username", help="Username of the NSX Manager.")
#     parser.add_argument("-p", "--password", help="Passowrd of the NSX Manager.")
#     args = parser.parse_args()
#     return args


def main():
    print(colored("Please Enter the IP of NSX-T Manager: ", 'yellow', attrs=['bold']))
    ip = input()
    print(colored("\nPlease Enter the username of NSX-T Manager: ", 'yellow', attrs=['bold']))
    username = input()
    print(colored("\nPlease Enter the password of NSX-T Manager: ", 'yellow', attrs=['bold']))
    password = input()
    print("-----------")
    nsx_client = NsxClient(ip)
    try:
        nsx_client.authorize(username, password)
    except requests.exceptions.ConnectionError:
        print(colored("You have a connection error to NSX-T manager,"
                          " please validate you details and try again", 'red', attrs=['bold']))
        exit_status = 1
        return exit_status
    except KeyError:
        print(colored("Invalid user and password, Please try again.", 'red', attrs=['bold']))
        exit_status = 1
        return exit_status
    except:
        print(colored("Please enter the NSX Manager details", 'red', attrs=['bold']))
        exit_status = 1
        return exit_status
    nsx_client.add_security_group()
    nsx_client.add_tags()


if __name__ == '__main__':
    main()

