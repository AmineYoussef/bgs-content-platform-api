import logging
from logging.handlers import TimedRotatingFileHandler
import os


class Logger:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
    )
    _instance = None

    def set_file_handler(cls, log_dir: str):
        """
        Set the file handler for logging in a given log directory

        Args:
            cls: class instance
            log_dir (str): The name of the collection to be initialized.

        Returns:
            None
        """
        file_handler = TimedRotatingFileHandler(
            "app.log", when="midnight", interval=1, backupCount=7
        )
        file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        cls._instance._logger.addHandler(file_handler)

    def __new__(cls, *args, **kwargs):
        """
        Create a logger instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._logger = logging.getLogger(__name__)

        return cls._instance

    def info(cls, message):
        """
        Log an info message to the logger

        Args:
            cls : class instance
            message (str): message to be logged

        Returns:
            None
        """
        cls._logger.info(message)

    def debug(cls, message):
        """
        Log a debug message to the logger

        Args:
            cls : class instance
            message (str): message to be logged

        Returns:
            None
        """
        cls._logger.debug(message)

    def warning(cls, message):
        """
        Log an warning message to the logger

        Args:
            cls : class instance
            message (str): message to be logged

        Returns:
            None
        """
        cls._logger.warning(message)

    def error(cls, message):
        """
        Log an error message to the logger

        Args:
            cls : class instance
            message (str): message to be logged

        Returns:
            None
        """
        cls._logger.error(message)

    def critical(cls, message):
        """
        Log a critical message to the logger

        Args:
            cls : class instance
            message (str): message to be logged

        Returns:
            None
        """
        cls._logger.critical(message)


logger = Logger()
