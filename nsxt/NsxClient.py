# This script recive 3 TXT files : env.txt, app.txt and os.txt.
# The files have to be in the same directory as the script.
# Files should contain the tags and scopes information for the security group.
# The script create a security groups in NSX-T base on the information that the files contain.

"""
 Example : 
	env.txt context --> prod
	app.txt context --> ishaiApp
	os.txt context --> linux
  The script will create a securiy group named "custom-prod-ishaiApp-linux" with 3 tag crateria (env: prod, app: ishaiApp and os: linux)
"""
# Wrriten by Ishai Shahak at 12/4/19

import requests
import json
import time
from IPython import embed
import argparse

requests.packages.urllib3.disable_warnings()  # Ignore from requests module warnings

ENV_FILE = "env.txt"
APP_FILE = "app.txt"
OS_FILE = "os.txt"

ADD_GROUP_URI = "api/v1/ns-groups"
AUTHORIZATION_URI = "api/session/create"


class NsxClient():

	def __init__(self, nsx_manager):
		self.session = requests.Session()
		self.nsx_manager = nsx_manager

		self.envFile = open(ENV_FILE, "r")
		self.rEnvFile = self.envFile.readlines()
		self.appFile = open(APP_FILE, "r")
		self.rAppFile = self.appFile.readlines()
		self.osFile = open(OS_FILE, "r")
		self.rOsFile = self.osFile.readlines()

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
		# Read the TXT files

		print ("")
		print("Strating to adding security groups...")
		print("")
		print("---------")
		print("")
		time.sleep(2)

		# REST API calls
		url = f"https://{self.nsx_manager}/{ADD_GROUP_URI}"

		for x in range(0,len(self.rAppFile)):

			strEnv = str(self.rEnvFile[x]).replace("\n", "")
			strApp = str(self.rAppFile[x]).replace("\n", "")
			strOs = str(self.rOsFile[x]).replace("\n", "")
			displayName = f"custom-{strEnv}-{strApp}-{strOs}"
			
			payload = {
				"display_name": displayName,
				"membership_criteria": [
					{
						"resource_type": "NSGroupComplexExpression",
						"expressions": [
						{
								"resource_type": "NSGroupTagExpression",
								"target_type": "VirtualMachine",
								"scope": "env",
								"tag": self.rEnvFile[x]
							},
							{
								"resource_type": "NSGroupTagExpression",
								"target_type": "VirtualMachine",
								"scope": "app",
								"tag": self.rAppFile[x]
							},
							{
								"resource_type": "NSGroupTagExpression",
								"target_type": "VirtualMachine",
								"scope": "os",
								"tag": self.rOsFile[x]
							}
						]
					}
				]
			}
			response = self.session.request("POST", url, data=json.dumps(payload), headers=self.headers, verify=False)
			
			if str(response.status_code) == "201":
				time.sleep(1)
				print ("Security group " + displayName + " added.")
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
		with open("vms.txt", 'r') as vms_file:
			vms = vms_file.readlines()

		for vm in vms:
			strvm = str(vm).replace("\n", "")
			url = f"https://{self.nsx_manager}/api/v1/fabric/virtual-machines?display_name={strvm}"
			payload = {}
			response = self.session.request("GET", url, headers=self.headers, data=json.dumps(payload), verify=False)
			to_json = response.json()
			results = to_json.get("results")
			vm_id = results[0].get("external_id")
			vm_ids.append(vm_id)

		return vm_ids

	def add_tags(self):
		vm_ids = self.get_vm_ids()
		for vm_id in vm_ids:
			url = f"https://{self.nsx_manager}/api/v1/fabric/virtual-machines?action=update_tags"
			for x in range(0, len(self.rAppFile)):
				payload = {
					"external_id": f"{vm_id}",
					"tags": [
						{"scope": "env", "tag": self.rEnvFile[x]},
						{"scope": "app", "tag": self.rAppFile[x]},
						{"scope": "os", "tag": self.rOsFile[x]}
					]
				}
				response = self.session.request("POST", url, headers=self.headers, data=json.dumps(payload), verify=False)
			if str(response.status_code) == "204":
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
	if oper not in range(1, 3):
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