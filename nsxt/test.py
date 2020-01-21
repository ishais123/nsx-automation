
import requests
import json
import argparse

requests.packages.urllib3.disable_warnings()  # Ignore from requests module warnings

GET_ROUTERS_URI = "api/v1/ns-groups"
AUTHORIZATION_URI = "api/session/create"

class NSX_CLIENT():
    def __init__(self, nsx_manager):
        self.session = requests.Session()
        self.nsx_manager = nsx_manager

    def authorize(self, username, password):
        self.username = username
        self.password = password
        url = "https://{}/{}".format(self.nsx_manager, AUTHORIZATION_URI)
        data = {"j_username": self.username, "j_password": self.password}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Allow-Overwrite': 'true'
        }
        response = self.session.request("POST", url, headers=headers, data=data, verify=False)
        self.xsrf_token = response.headers['X-XSRF-TOKEN']
    
    def get_routers(self):
        url = "https://{}/{}".format(self.nsx_manager, GET_ROUTERS_URI)
        headers = {
            'Content-Type': "application/json",
            'Host': self.nsx_manager,
            'X-XSRF-TOKEN': self.xsrf_token
        }
        response = self.session.request("GET", url, headers=headers, verify=False)
        with open("nsgroup.txt", "w") as f:
            f.write(response.text)

def parse_args():
	parser = argparse.ArgumentParser(description='Enter IP, Username and Password of NSX Node.')
	parser.add_argument("-i", "--ip", help="IP address of the NSX Manager.")
	parser.add_argument("-u", "--username", help="Username of the NSX Manager.")
	parser.add_argument("-p", "--password", help="Passowrd of the NSX Manager.")
	args = parser.parse_args()
	return args

def main():
    args = parse_args()
    client = NSX_CLIENT(args.ip)
    client.authorize(args.username, args.password)
    client.get_routers()

if __name__ == '__main__':
	main()
    
