__author__ = 'Iacopo Papalini <iacopo@domotz.com>'
import datetime
from json import JSONEncoder

import json


class JsonWriter(object):
    def write(self, file_handler, data):
        data_ = json.dumps(data, cls=MyJSONEncoder, indent=2)
        file_handler.write(data_.encode('utf-8'))


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.replace(microsecond=0).isoformat()
        try:
            return o.data
        except AttributeError:
            return super(MyJSONEncoder, self).default(o)
