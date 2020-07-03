__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

import asyncio
import json
import logging
from argparse import ArgumentParser
from os.path import dirname, expanduser

from domotz_camera_tool.client import ApiClient
from domotz_camera_tool.commands import list_agents, list_cameras, take_snapshot, compose, generate_config_file
from domotz_camera_tool.commands.generate_config_file import DEFAULT_CONFIG_FILE

COMMANDS = (list_agents, list_cameras, take_snapshot, compose, generate_config_file)

DESCRIPTION = ''
HERE = dirname(__file__)


def load_configuration(args):
    logger = logging.getLogger()
    try:
        with open(args.configuration) as configuration_file:
            configuration = json.load(configuration_file)
            logger.debug("Configuration file %s loaded", args.configuration)
    except OSError as e:
        logger.debug("Cannot load configuration file %s: %s", args.configuration, e)
        configuration = {}
    if args.api_key:
        configuration['api_key'] = args.api_key
    if args.endpoint:
        configuration['endpoint'] = args.endpoint

    if not configuration.get('api_key', None):
        raise RuntimeError("api_key", "Missing either in configuration file or as parameter")
    if not configuration.get('endpoint', None):
        raise RuntimeError("endpoint", "Missing either in configuration file or as parameter")
    return configuration


def main():
    parser = ArgumentParser(description=DESCRIPTION)
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S ')
    logger = logging.getLogger()

    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
    parser.add_argument('-c', '--configuration', default=DEFAULT_CONFIG_FILE,
                        required=False,
                        help="The path of the configuration file: it must be a json file with two keys: \"api_key\" "
                             "and \"endpoint\"")
    parser.add_argument('-k', '--api_key', default=None, required=False,
                        help="The API key (overrides the configuration)")
    parser.add_argument('-e', '--endpoint', default=None, required=False,
                        help="The endpoint (overrides the configuration)")
    subparsers = parser.add_subparsers()

    for module in COMMANDS:
        module.add_command(subparsers)

    args = parser.parse_args()
    if args.verbosity >= 2:
        logger.setLevel(logging.DEBUG)
        requests_log = logging.getLogger("urllib3.connectionpool")
        requests_log.setLevel(logging.INFO)
        requests_log.propagate = False
    elif args.verbosity == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    if 'function' in args and args.function != generate_config_file.action:
        configuration = load_configuration(args)
        client = ApiClient(**configuration)
    else:
        client = None
    try:
        callable_ = args.function
    except AttributeError:
        print(parser.format_usage())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(callable_(args, client))


if __name__ == '__main__':
    main()
