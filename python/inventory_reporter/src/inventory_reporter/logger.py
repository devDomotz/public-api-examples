import logging
from logging import FileHandler, Formatter

from colorlog import ColoredFormatter, StreamHandler

__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class LogCreator:
    def __init__(self, configuration):
        self.configuration = configuration

    def initialize_logging(self):
        log_level = self.configuration.get('level', 'DEBUG')
        file_name = self.configuration.get('file')
        if file_name:
            handler = self._file_handler(file_name)
        else:
            handler = self._terminal_handler()

        log = logging.getLogger()
        log.setLevel(log_level)

        log.addHandler(handler)
        return log

    @classmethod
    def _file_handler(cls, file_name):
        handler = FileHandler(filename=file_name)
        handler.setFormatter(Formatter(fmt='[%(levelname).1s %(asctime)s] %(message)s',
                                       datefmt=LOG_DATE_FORMAT))
        return handler

    @classmethod
    def _terminal_handler(cls):
        handler = StreamHandler()
        handler.setFormatter(cls._terminal_formatter())
        return handler

    @classmethod
    def _terminal_formatter(cls):
        formatter = ColoredFormatter(
            fmt='%(log_color)s[%(levelname).1s %(asctime)s]%(reset)s %(message)s',
            datefmt=LOG_DATE_FORMAT,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={}
        )
        return formatter
