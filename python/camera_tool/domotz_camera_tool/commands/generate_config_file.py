from __future__ import annotations

import json
import logging
from os.path import expanduser

from domotz_camera_tool.client import ApiClient

__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

_logger = logging.getLogger(__name__)

DESCRIPTION = "Generates a configuration file in order to not insert API key and endpoint again."
COMMAND_NAME = 'generate-config'
DEFAULT_CONFIG_FILE = expanduser('~/.domotz_camera_tools.config.json')


def add_command(subparsers):
    parser = subparsers.add_parser(COMMAND_NAME, help=DESCRIPTION)
    parser.add_argument('api_key', default=None, help="The api key")
    parser.add_argument('endpoint', default=None, help="The endpoint URL")

    parser.set_defaults(function=action)


async def action(args, _):
    data = {
        'api_key': args.api_key,
        'endpoint': args.endpoint
    }
    client = ApiClient(**data)
    await client.get_json('meta', 'usage')
    with open(DEFAULT_CONFIG_FILE, 'w') as f:
        f.write(json.dumps(data, indent=2))
    print(f"Stored valid configuration in {DEFAULT_CONFIG_FILE}")