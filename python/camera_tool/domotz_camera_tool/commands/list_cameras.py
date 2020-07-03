from __future__ import annotations

import logging

from tabulate import tabulate

from domotz_camera_tool.client import ApiClient

__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

from domotz_camera_tool.helpers.cameras import CamerasHelper

_logger = logging.getLogger(__name__)

DESCRIPTION = "Lists the cameras on the agent"
COMMAND_NAME = 'list-cameras'


def add_command(subparsers):
    parser = subparsers.add_parser(COMMAND_NAME, help=DESCRIPTION)
    parser.add_argument('agent_id', default=None, help="The Id of the agent")

    parser.set_defaults(function=_list_cameras)


async def _list_cameras(args, client: ApiClient):
    agent_id = args.agent_id
    cameras = await CamerasHelper(client).fetch_cameras(agent_id)
    print(tabulate(cameras, headers=['Id', 'Name', 'Ip Address', 'Make', 'Model', 'Status']))
