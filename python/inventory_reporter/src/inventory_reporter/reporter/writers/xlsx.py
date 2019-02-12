from datetime import datetime, timedelta
from io import BytesIO

from xlsxwriter import Workbook

__author__ = 'Iacopo Papalini <iacopo@domotz.com>'


class ExcelWriter(object):
    def __init__(self):
        self._new_device_threshold = datetime.utcnow() - timedelta(days=30)

    def write(self, file_handler, data):
        output = BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        self._write(workbook, data)
        workbook.close()
        file_handler.write(output.getvalue())

    def _write(self, workbook, data):
        worksheet = workbook.add_worksheet("All Assets")

        current_row_index = self._write_header(worksheet, workbook)
        for agent in data:
            for device in agent.devices:
                record = Record(agent, device, self._new_device_threshold)
                current_row_index = self._write_record(current_row_index, record, worksheet)

    def _write_record(self, current_row_index, record, worksheet):
        worksheet.write_row(current_row_index, 0, (
            record.agent_name,
            record.zone or 'Unknown',
            record.location or 'Unknown',
            record.ip_addresses,
            record.hw_address,
            record.display_name,
            record.vendor,
            record.model,
            record.first_seen_on,
            record.last_seen_if_offline,
            record.tags))
        return current_row_index + 1

    def _write_header(self, worksheet, workbook):
        date_format = workbook.add_format()
        date_format.set_num_format('yyyy-mm-dd')
        data = (
            ('Site', 15, None),
            ('Zone', 12, None),
            ('Location', 12, None),
            ('Network Address(es)', 14, None),
            ('HW Address', 16, None),
            ('Asset Name', 24, None),
            ('Vendor', 16, None),
            ('Model', 16, None),
            ('First seen on', 12, date_format),
            ('Last seen if offline', 12, date_format),
            ('Tags', 30, None)
        )

        worksheet.write_row(0, 0, (_[0] for _ in data))
        for col, (_, size, format_) in enumerate(data):
            worksheet.set_column(col, col, size, format_)

        return 1


class Record:
    def __init__(self, agent, device, new_device_threshold):
        self._new_device_threshold = new_device_threshold
        self.agent = agent
        self.device = device

    @property
    def agent_name(self):
        return self.agent.display_name

    @property
    def zone(self):
        return self.device.get('details.zone')

    @property
    def location(self):
        return self.device.get('details.zone')

    @property
    def ip_addresses(self):
        return ','.join(self.device.get('ip_addresses') or [])

    @property
    def hw_address(self):
        return self.device.hw_address

    @property
    def display_name(self):
        return self.device.display_name

    @property
    def first_seen_on(self):
        return self.parse_datetime(self.device.first_seen_on)

    @property
    def last_seen_if_offline(self):
        return self.parse_datetime(self.device.last_status_change if not self.device.is_online else None)

    @property
    def vendor(self):
        return self.device.get('user_data.vendor') or self.device.vendor

    @property
    def model(self):
        return self.device.get('user_data.model') or self.device.model

    @property
    def tags(self):
        tags = []
        if not self.zone and not self.location:
            tags.append('no_place')
        if self.parse_datetime(self.device.first_seen_on) > self._new_device_threshold:
            tags.append('new')
        return ','.join(tags)

    @classmethod
    def parse_datetime(cls, datetime_str):
        try:
            if datetime_str[-6:] == '+00:00':
                datetime_str = datetime_str[:-6]

            return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")

        except (ValueError, TypeError):
            return None
