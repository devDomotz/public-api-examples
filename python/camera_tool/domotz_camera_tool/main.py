__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

import asyncio
import json
import logging
from argparse import ArgumentParser
from os.path import dirname

from domotz_camera_tool.client import ApiClient
from domotz_camera_tool.commands import list_agents, list_cameras, take_snapshot, compose, generate_config_file
from domotz_camera_tool.commands.generate_config_file import DEFAULT_CONFIG_FILE

MANDATORY_PARAMETERS = 'api_key', 'endpoint'

COMMANDS = (list_agents, list_cameras, take_snapshot, compose, generate_config_file)

DESCRIPTION = ''
HERE = dirname(__file__)


def main():
    parser = ArgumentParser(description=DESCRIPTION)

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

    configure_logger(args)
    client = create_client(args)
    try:
        callable_ = args.function
    except AttributeError:
        print(parser.format_usage())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(callable_(args, client))


def configure_logger(args):
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S ')
    logger = logging.getLogger()
    if args.verbosity >= 2:
        logger.setLevel(logging.DEBUG)
        requests_log = logging.getLogger("urllib3.connectionpool")
        requests_log.setLevel(logging.INFO)
        requests_log.propagate = False
    elif args.verbosity == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)


def create_client(args):
    # pylint: disable=comparison-with-callable
    if 'function' in args and args.function != generate_config_file.action:
        configuration = load_configuration(args)
        client = ApiClient(**configuration)
    else:
        client = None
    return client


def load_configuration(args):
    logger = logging.getLogger()
    try:
        with open(args.configuration) as configuration_file:
            configuration = json.load(configuration_file)
            logger.debug("Configuration file %s loaded", args.configuration)
    except OSError as e:
        logger.debug("Cannot load configuration file %s: %s", args.configuration, e)
        configuration = {}

    override_parameters(args, configuration)
    check_mandatory_parameters(configuration)
    return configuration


def check_mandatory_parameters(configuration):
    for parameter in MANDATORY_PARAMETERS:
        if not configuration.get(parameter, None):
            raise RuntimeError(parameter, "Missing either in configuration file or as parameter")


def override_parameters(args, configuration):
    for parameter in MANDATORY_PARAMETERS:
        if parameter in args:
            configuration[parameter] = args[parameter]


if __name__ == '__main__':
    main()
