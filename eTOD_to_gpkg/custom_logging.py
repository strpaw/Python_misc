"""Set custom logging"""
import os.path
import logging
from logging.handlers import TimedRotatingFileHandler


def configure_logging(file_name: str = "log.txt") -> None:
    """Set logging configuration.

    :param file_name: log file name
    :type file_name: str
    """
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join('logs', file_name),
        when="MIDNIGHT",
        backupCount=7
    )
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.INFO,
        handlers=[file_handler]
    )
