NsxClient Tool
==============

Python tool for automatic security groups and security tags creation, This tool leveraging NSX-T 2.5 REST API.

It can be very helpful tool to automate the security fabric creation phase in NSX-T MicroSegmentation projects.

### NOTE:

This tool get a CSV file and create the relevant objects according to it.

Put the "mapping.csv" in the same directory as the tool file. (Example CSV file exists in "NsxClient_v3" directory)

### HOW TO:

To run this tool please use command structure below:

python NsxClient_v3.py -i [nsx_manager_ip] -u [nsx_manager_user] -p [nsx_manager_password]

