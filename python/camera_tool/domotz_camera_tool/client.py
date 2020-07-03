__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

import logging

import aiohttp

_logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, endpoint, api_key, **_):
        self.endpoint = endpoint
        self.api_key = api_key
        self._headers = {"X-Api-Key": self.api_key}

    async def get_json(self, *steps, message=None) -> dict:
        return await self._get('json', *steps, message=message)

    async def get_bytes(self, *steps, message=None) -> bytes:
        return await self._get('read', *steps, message=message)

    async def _get(self, decoder, *steps, message=None):
        url = self.endpoint + "/".join(map(str, steps))

        async with aiohttp.ClientSession() as session:
            if message:
                _logger.info(message)
            else:
                _logger.info("Performing GET on %s", url)
            async with session.get(url, headers=self._headers) as response:
                if response.status > 299:
                    raise RuntimeError(response.status, await response.text())
                _logger.debug("Status code: %s", response.status)
                return await response.__getattribute__(decoder)()

    async def fetch_devices(self, agent_id):
        devices_raw = await self.get_json('agent', agent_id, 'device',
                                          message="Fetching device list for agent {}".format(
                                              agent_id))
        return devices_raw

    async def fetch_device_details(self, agent_id, device_id):
        return await self.get_json('agent', agent_id, 'device', device_id,
                                   message="Fetching details for device {}".format(device_id))

    async def fetch_agent_details(self, agent_id):
        return await self.get_json('agent', agent_id, message="Fetching details for agent {}".format(agent_id))
