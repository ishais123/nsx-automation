NsxClient Tool
==============

Python tool for automatic Security groups and tags creation, This tool leveraging NSX-T REST API.

NOTE:
^^^^^

This tool get a CSV file and create the relevant objects according to it.

Put the "mapping.csv" in the sane directory as the tool file. (Example CSV file exists in "NsxClient_v3" directory)

HOW TO:
=======

To run this tool please use command structure below:

python NsxClient_v3.py -i [nsx_manager_ip] -u [nsx_manager_user] -p [nsx_manager_password]

