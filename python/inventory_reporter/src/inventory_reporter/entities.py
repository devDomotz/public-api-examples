__author__ = 'Iacopo Papalini <iacopo@domotz.com>'


class BaseEntity:
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def id(self):
        return self._data['id']

    def __getattr__(self, item):
        return self._data.get(item)

    def get(self, path):
        path = path.split('.')
        data = self.data
        for step in path:
            if step not in data:
                return None
            data = data[step]
        return data


class Agent(BaseEntity):
    @property
    def can_be_accessed(self):
        rights = self.data.get('access_right', {})
        return rights.get('api_enabled', False)

    def set_devices(self, devices):
        self.data['devices'] = devices


class Device(BaseEntity):
    @property
    def is_online(self):
        return self._data.get('status') == 'ONLINE'
