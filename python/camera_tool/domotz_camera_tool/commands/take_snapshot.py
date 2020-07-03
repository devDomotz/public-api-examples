from __future__ import annotations

import logging
from datetime import datetime

from domotz_camera_tool.client import ApiClient

__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

from domotz_camera_tool.helpers.cameras import CamerasHelper

_logger = logging.getLogger(__name__)

DESCRIPTION = "Takes a snapshot from a camera"
COMMAND_NAME = 'snapshot'


def add_command(subparsers):
    parser = subparsers.add_parser(COMMAND_NAME, help=DESCRIPTION)
    parser.add_argument('agent_id', default=None, help="The Id of the agent")
    parser.add_argument('camera_id', default=None, help="The device Id of the camera")

    parser.set_defaults(function=_snapshot)


async def _snapshot(args, client: ApiClient):
    agent_id = args.agent_id
    device_id = args.camera_id
    image = await CamerasHelper(client).get_snapshot(agent_id, device_id)

    file_name = "{}-{}.{}".format(device_id, datetime.now().isoformat(timespec='seconds'), image.format.lower())
    image.save(file_name)

    _logger.info("Saved file %s (%s)", file_name, image.size)
