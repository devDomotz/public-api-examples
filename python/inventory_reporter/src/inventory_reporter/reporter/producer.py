import datetime
import logging
import sys

from inventory_reporter.reporter.writers.json_ import JsonWriter
from inventory_reporter.reporter.writers.xlsx import ExcelWriter

__author__ = 'Iacopo Papalini <iacopo@domotz.com>'


class ReportProducer:
    def __init__(self, configuration, public_api_client):
        self.configuration = configuration
        self.public_api_client = public_api_client

    async def produce_report(self):
        data = await self._fetch_data()
        file_handler = self._get_file_handler()
        try:
            self.get_renderer(self.configuration.get('report', {}).get('format'))().write(file_handler, data)
        finally:
            if file_handler != sys.stdout:
                file_handler.close()

    def _get_file_handler(self):
        file_name = self.configuration.get('report', {}).get('file_name', None)
        if not file_name:
            logging.warning("No file specified, writing to stdout")
            return sys.stdout.buffer
        else:
            file_name = file_name.replace('{{date}}', datetime.datetime.now().replace(microsecond=0).isoformat())
            logging.info("Writing on {}".format(file_name))
            return open(file_name, 'wb')

    async def _fetch_data(self):
        agents = await self.public_api_client.get_agents()
        ret = []
        for agent in agents:
            if not agent.can_be_accessed:
                logging.warning("Skipping agent {} {}: cannot access it through Public API".format(
                    agent.id, agent.display_name))
                continue
            logging.info("Loading devices for agent '{}'".format(agent.display_name))
            tmp = await self.public_api_client.get_devices(agent.id)
            devices = []
            for device in tmp or []:
                devices.append(await self.public_api_client.get_device(agent.id, device.id))
            agent.set_devices(devices)
            ret.append(agent)
            logging.info("{} devices loaded".format(len(devices)))
        return ret

    def get_renderer(self, output_type):
        plugin = {
            'xlsx': ExcelWriter,
            'json': JsonWriter
        }.get(output_type, None)

        if not plugin:
            raise RuntimeError("{} type not supported".format(output_type))

        return plugin
