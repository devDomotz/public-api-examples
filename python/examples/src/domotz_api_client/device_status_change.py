__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

import csv
import logging
import requests
import sys
from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime, timedelta

DESCRIPTION = "Reports, as cvs file, all the device status changes in a given period for an agent"
delta = timedelta(days=30)

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

    def get_device_history(self, agent_id, device_id, from_: datetime, to: datetime):
        url = '/'.join((self.base_url, 'agent', str(agent_id), 'device', str(device_id), 'history', 'network', 'event'))

        params = {'from': from_.isoformat()+'T00:00:00', 'to': to.isoformat()+'T00:00:00'}
        response = requests.get(url, params=params, headers=self._headers())
        if response.status_code != 200:
            _logger.error("URL: %s", url)
            _logger.error("Params: %s", params)
            raise RuntimeError(response.text)
        return response.json()


def report_device_status_changes(agent_id, from_, to, api_wrapper):
    devices = api_wrapper.get_device_list(agent_id)
    history = []
    for device in devices:
        history += retrieve_full_device_list(agent_id, device, from_, to, api_wrapper)
    return sorted(history, key=lambda x: (x[0], x[-1]))


def retrieve_full_device_list(agent_id, device, from_, to, api_wrapper):
    if device['protocol'] != 'IP':
        _logger.info("Ignoring device %s of type %s", device['id'], device['protocol'])
        return []

    _logger.info("Retrieving history for device %s", device['id'])
    device_history = []
    tmp_to = min(from_ + delta, to)
    while True:
        _logger.debug("Retrieving history for device %s from %s to %s", device['id'], from_, to)
        device_history += get_and_filter_device_history_interval(agent_id, device, from_, tmp_to, api_wrapper)
        from_ = tmp_to
        tmp_to = min(from_ + delta, to)
        if from_ == tmp_to:
            break
    return device_history


def get_and_filter_device_history_interval(agent_id, device, from_, to, api_wrapper):
    device_history_for_interval = []
    device_data = (
        device['display_name'], device['vendor'], device['hw_address'], device['ip_addresses'][0], device['id'])
    tmp_device_history = api_wrapper.get_device_history(agent_id, device['id'], from_, to)
    for event in tmp_device_history:
        if event['type'] in ('UP', 'DOWN'):
            device_history_for_interval.append((event['timestamp'], event['type']) + device_data)
        else:
            _logger.info("Ignoring event %s for device %s", event['type'], device['id'])
    return device_history_for_interval


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise ArgumentTypeError(msg)


if __name__ == '__main__':
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument('agent_id', help='Agent Id')
    parser.add_argument('from_', help='From (format yyyy-mm-dd', metavar='from', type=valid_date)
    parser.add_argument('to', help='To (format yyyy-mm-dd', type=valid_date)
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
