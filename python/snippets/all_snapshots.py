# Basic example for taking snapshots from all the online, unlocked cameras of an agent
# API endpoint and key are passed as first and second command line parameter
# Agent id is passed as third parameter
import sys

import requests

endpoint = sys.argv[1]
api_key = sys.argv[2]
agent_id = sys.argv[3]

types = requests.get(endpoint + 'type/device/detected', headers={'X-Api-Key': api_key}).json()

camera_types = []
for type_ in types:
    if 'snapshot' in type_['capabilities']:
        camera_types.append(type_['id'])

all_devices = requests.get(endpoint + f'agent/{agent_id}/device', headers={'X-Api-Key': api_key}).json()


def handle_device(device):
    response = requests.get(
        endpoint + f"agent/{agent_id}/device/{device['id']}/multimedia/camera/snapshot",
        headers={'X-Api-Key': api_key})

    extension = response.headers['content-type'].split('/')[-1]
    file_name = f"{device['display_name']}.{extension}"
    with open(file_name, 'wb') as image:
        image.write(response.content)


for device in all_devices:
    if 'ONLINE' == device['status'] and device.get('type', {}).get('detected_id', 0) in camera_types:
        device = requests.get(
            endpoint + f"agent/{agent_id}/device/{device['id']}",
            headers={'X-Api-Key': api_key}).json()

        if device.get('authentication_status', '') in ('AUTHENTICATED', 'NO_AUTHENTICATION'):
            handle_device(device)
