import json
import logging

import aiohttp
from aiohttp import ClientTimeout

from inventory_reporter.entities import Agent, Device

__author__ = 'Iacopo Papalini <iacopo@domotz.com>'


class DomotzPublicAPIClient:
    TIMEOUT = ClientTimeout(total=10)

    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self._session = aiohttp.ClientSession(timeout=self.TIMEOUT, headers={'X-API-Key': api_key})

    async def shutdown(self):
        logging.info("Shutting down API client")
        await self._session.close()

    async def get_agents(self):
        logging.debug("Recovering agents list")
        ret = await self._session.get("{}agent".format(self.endpoint))
        data = await ret.json()
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(json.dumps(data, sort_keys=True))
        ret = [Agent(_) for _ in data]
        return ret

    async def get_devices(self, agent_id):
        logging.debug("Recovering device list for agent %s", agent_id)
        ret = await self._session.get("{}agent/{}/device".format(self.endpoint, agent_id))
        data = await ret.json()
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(json.dumps(data, sort_keys=True))
        ret = [Device(_) for _ in data]
        return ret

    async def get_device(self, agent_id, device_id):
        logging.debug("Recovering device %s for agent %s", device_id, agent_id)
        ret = await self._session.get("{}agent/{}/device/{}".format(self.endpoint, agent_id, device_id))
        data = await ret.json()
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(json.dumps(data, sort_keys=True))
        return Device(data)

    async def change_device_field(self, agent_id, device_id, field_name, value):
        logging.debug("Setting field `%s`=`%s` for device %s", field_name, value, device_id)
        await self._session.put('{}agent/{}/device/{}/{}'.format(self.endpoint, agent_id, device_id, field_name),
                                json=value)

    async def hide_device(self, agent_id, device_id):
        logging.debug("Hiding device {}".format(device_id))
        await self._session.delete('{}agent/{}/device/{}'.format(self.endpoint, agent_id, device_id))
