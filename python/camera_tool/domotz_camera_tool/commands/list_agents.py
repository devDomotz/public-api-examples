from __future__ import annotations

from collections import namedtuple

from tabulate import tabulate

from domotz_camera_tool.client import ApiClient

__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

DESCRIPTION = "Lists the agents"
COMMAND_NAME = 'list-agents'

Agent = namedtuple('Agent', 'id,name,api_enabled,status')


def add_command(subparsers):
    parser = subparsers.add_parser(COMMAND_NAME, help=DESCRIPTION)

    parser.set_defaults(function=_list_agents)


async def _list_agents(args, client: ApiClient):
    agents_raw = await client.get_json('agent', message="Retrieving all agents")
    agents = []
    for data in agents_raw or []:
        agents.append(Agent(data['id'], data['display_name'], data['access_right']['api_enabled'],
                            data['status']['value']))
    agents = sorted(agents, key=lambda x: (not x.api_enabled, x.name))
    print(tabulate(agents, headers=['Id', 'Name', 'Api Enabled', 'Status']))
