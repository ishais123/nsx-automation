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
from IPython import embed
import argparse
import pandas

requests.packages.urllib3.disable_warnings()  # Ignore from requests module warnings

MAPPING_FILE = 'mapping.csv'
VMS_FILE = 'vms.txt'

ADD_GROUP_URI = "api/v1/ns-groups"
AUTHORIZATION_URI = "api/session/create"
ADD_TAGS_URI = "api/v1/fabric/virtual-machines?action=update_tags"


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

	def add_security_group(self):
		print ("")
		print("Starting to adding security groups...")
		print("")
		print("---------")
		print("")
		time.sleep(2)

		# REST API calls
		url = f"https://{self.nsx_manager}/{ADD_GROUP_URI}"

		for x in range(0, len(self.mapping['ENV'])):
			env_tag = self.mapping['ENV'][x]
			app_tag = self.mapping['APP'][x]
			os_tag = self.mapping['OS'][x]
			display_name = f"custom-{env_tag}-{app_tag}-{os_tag}"
			
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
				time.sleep(1)
				print("Security group " + display_name + " added.")
			else:
				print(response.text)
				
		if str(response.status_code) == "201":
			time.sleep(2)
			print("")
			print("---------")
			print("")
			print ("All Security groups added.")

	def get_vm_ids(self):
		vm_ids = []
		with open(VMS_FILE, 'r') as vms_file:
			vms = vms_file.readlines()

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

	def add_tags(self):
		vm_ids = self.get_vm_ids()
		seq = int(input("Please enter the squence number of SG group that you want to add your VM's:  "))
		count = 0
		for vm_id in vm_ids:
			url = f"https://{self.nsx_manager}/{ADD_TAGS_URI}"
			payload = {
				"external_id": f"{vm_id}",
				"tags": [
					{"scope": "env", "tag": self.mapping['ENV'][seq-1]},
					{"scope": "app", "tag": self.mapping['APP'][seq-1]},
					{"scope": "os", "tag": self.mapping['OS'][seq-1]}
				]
			}
			response = self.session.request("POST", url, headers=self.headers, data=json.dumps(payload), verify=False)
			if str(response.status_code) != "204":
				count = count + 1
		if count == 0:
			time.sleep(2)
			print("All tags added!!!")


def parse_args():
	parser = argparse.ArgumentParser(description='Enter IP, Username and Password of NSX Node.')
	parser.add_argument("-i", "--ip", help="IP address of the NSX Manager.")
	parser.add_argument("-u", "--username", help="Username of the NSX Manager.")
	parser.add_argument("-p", "--password", help="Passowrd of the NSX Manager.")
	args = parser.parse_args()
	return args


def main():
	args = parse_args()
	nsx_client = NsxClient(args.ip)
	nsx_client.authorize(args.username, args.password)
	print("-----Hello and welcome to AutoNSX tool-----")
	oper = int(input("\nPlease Choose the operation:\n"
							 "1. Add Security groups\n"
							 "2. Add security tags\n"
							 "3. Add Segments\n"))
	if oper not in range(1, 4):
		exit_status = 1
		print("Please choose valid operation")
		return exit_status
	if oper == 1:
		nsx_client.add_security_group()
	if oper == 2:
		nsx_client.add_tags()
	if oper == 3:
		print("sorry but automation not finish currently") # will be nsx_client.add_segment()


if __name__ == '__main__':
	main()
