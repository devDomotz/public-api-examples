# Basic example for listing online agents name
# API endpoint and key are passed as first and second command line parameter
import sys, requests

endpoint = sys.argv[1]
api_key = sys.argv[2]

agents = requests.get(endpoint + 'agent', headers={'X-Api-Key': api_key}).json()

for agent in agents:
    if agent['status']['value'] != 'ONLINE' or not agent['access_right']['api_enabled']:
        continue
    print(agent['display_name'], agent['id'])
