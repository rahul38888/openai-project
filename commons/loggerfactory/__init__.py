import logging
import logging.config
from logging import Logger
from pathlib import Path


class LoggerFactory:
    def __init__(self, file: str | Path):
        """
        Logger factory to simplify
        :param file: Logger config file
        """
        logging.config.fileConfig(file)

    @staticmethod
    def getLogger(name: str) -> Logger:
        """
        A static method to get logger
        :param name: Name of the logger
        @return: Logger
        """
        return logging.getLogger(name)
