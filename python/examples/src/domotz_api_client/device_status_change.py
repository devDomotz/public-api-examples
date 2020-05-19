__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

import csv
import logging
import sys
from argparse import ArgumentParser

import requests

DESCRIPTION = "Reports, as cvs file, all the device status changes in a given period for an agent"

_logger = logging.getLogger(__name__)


class ApiWrapper:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def _headers(self):
        return {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        }

    def get_device_list(self, agent_id):
        url = '/'.join((self.base_url, 'agent', str(agent_id), 'device'))
        response = requests.get(url, headers=self._headers())
        return response.json()

    def get_device_history(self, agent_id, device_id, from_, to):
        url = '/'.join((self.base_url, 'agent', str(agent_id), 'device', str(device_id), 'history', 'network', 'event'))
        response = requests.get(url, params={'from': from_, 'to': to}, headers=self._headers())
        return response.json()


def report_device_status_changes(agent_id, from_, to, api_wrapper):
    devices = api_wrapper.get_device_list(agent_id)
    history = []
    for device in devices:
        if device['protocol'] != 'IP':
            _logger.info("Ignoring device %s of type %s", device['id'], device['protocol'])
            continue
        device_data = (
        device['display_name'], device['vendor'], device['hw_address'], device['ip_addresses'][0], device['id'])
        _logger.info("Retrieving history for device %s", device['id'])
        device_history = api_wrapper.get_device_history(agent_id, device['id'], from_, to)
        for event in device_history:
            if event['type'] in ('UP', 'DOWN'):
                history.append((event['timestamp'], event['type']) + device_data)
            else:
                _logger.info("Ignoring event %s for device %s", event['type'], device['id'])

    return sorted(history, key=lambda x: (x[0], x[-1]))


if __name__ == '__main__':
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument('agent_id', help='Agent Id')
    parser.add_argument('from_', help='From (format yyyy-mm-dd', metavar='from')
    parser.add_argument('to', help='To (format yyyy-mm-dd')
    parser.add_argument('base_url',
                        help='Base URL, as obtained from https://portal.domotz.com/portal/settings/services')
    parser.add_argument('api_key', help='Api Key')
    logging.basicConfig()
    logger = logging.getLogger()

    parser.add_argument('-v', '--verbose', action='store_true', help="Set verbose output on stderr")
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    writer = csv.writer(sys.stdout)
    writer.writerow(('Timestamp', 'Event', 'Name', 'Make', 'MAC Address', 'Main IP address', 'Id'))
    for event in report_device_status_changes(args.agent_id, args.from_, args.to,
                                              ApiWrapper(args.base_url, args.api_key)):
        writer.writerow(event)
