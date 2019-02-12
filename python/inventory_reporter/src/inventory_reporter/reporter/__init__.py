import argparse
import asyncio
import signal
import traceback

from colorlog import logging

from inventory_reporter.api_client import DomotzPublicAPIClient
from inventory_reporter.logger import LogCreator
from inventory_reporter.reporter.producer import ReportProducer

__author__ = 'Iacopo Papalini <iacopo@domotz.com>'


class Runner:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.public_api_client = None

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser(
            description='Creates a report of a Domotz Inventory - lists all devices on every agent')

        parser.add_argument('-u', '--endpoint-url', required=True,
                            help="API endpoint e.g. https://api-eu-west-1-cell-1.domotz.com/public-api/v1/")
        parser.add_argument('-k', '--api-key', required=True, help="Your secret API key")
        parser.add_argument('-v', '--verbose', action='store_true', help="More verbose log")
        parser.add_argument('-f', '--format', required=False, default='xlsx', help="Output format, either xlsx or json")
        parser.add_argument('-o', '--output-file', required=False, default=None,
                            help="Output file, if not given stdout will be used")
        parser.add_argument('-l', '--log-file', required=False, default=None,
                            help="Log file, if not given stderr will be used")
        arguments = parser.parse_args()

        configuration = {
            'log': {
                'level': 'INFO',
                'file_name': arguments.log_file
            },
            "api-endpoint": arguments.endpoint_url,
            "api-key": arguments.api_key,
            "report": {
                'format': arguments.format,
                'file_name': arguments.output_file
            }

        }
        if arguments.verbose:
            configuration['log']['level'] = 'DEBUG'

        Runner().startup(configuration)

    def startup(self, configuration):
        self.loop.create_task(self.run(configuration))
        self.loop.run_forever()

    async def run(self, configuration):
        LogCreator(configuration['log']).initialize_logging()
        logging.info("Initializing resources")
        self.public_api_client = DomotzPublicAPIClient(configuration['api-endpoint'],
                                                       configuration['api-key'])
        self.loop.add_signal_handler(signal.SIGINT, self.end)
        self.loop.add_signal_handler(signal.SIGTERM, self.end)
        producer = ReportProducer(configuration, self.public_api_client)
        try:
            await producer.produce_report()
            await self._cleanup()
        except Exception:
            logging.error(traceback.format_exc())
            self.end()

    def end(self, *_):
        logging.warning('SIGINT or SIGTERM handled')
        self.loop.create_task(self._cleanup())

    async def _cleanup(self):
        logging.debug('Cleaning up before closing')
        if self.public_api_client:
            await self.public_api_client.shutdown()
        self.loop.stop()
        logging.debug('Clean up done')
