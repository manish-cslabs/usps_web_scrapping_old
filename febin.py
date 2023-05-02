import requests

from config import *

from requests.auth import HTTPBasicAuth



usps_user_name='aci.usps.devteam'

usps_user_password='MFH1bmq6cea!bzv?ruk'


headers = {'content-type': 'application/json'}

usps_url_list_of_all_outbound_file = f'https://pdx.usps.com/api/extracts?environment={environment}&fileType={fileType}&fullList={fullList}&fromDate={fromDate}&toDate={toDate}'

response = requests.get(usps_url_list_of_all_outbound_file, auth=HTTPBasicAuth(usps_user_name, usps_user_password), headers=headers, verify=False)

print(response)