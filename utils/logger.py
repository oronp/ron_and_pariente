import logging
import sys
from typing import Optional, Dict

from utils.color_formatter import ColorFormatter


class SingletonMeta(type):
    """
    A metaclass that creates a Singleton base type when called.
    """
    _instances: Dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Create and store the instance if it doesn't exist
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ChatLogger(metaclass=SingletonMeta):
    """
    A singleton logger class for consistent logging across the application.
    """

    def __init__(self, logger_name: str = 'DefaultLogger'):
        # To prevent reinitialization in case of multiple calls
        if hasattr(self, '_initialized') and self._initialized:
            return

        # Create a custom logger with the provided name
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)  # Set the minimum log level

        # Avoid adding multiple handlers if they already exist
        if not self.logger.hasHandlers():
            # Create console handler for logging to stdout
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)

            # Apply colored formatter for console logs
            color_formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(color_formatter)

            # add file handlers or other handlers here if needed
            # file_handler = logging.FileHandler('app.log')
            # file_handler.setLevel(logging.INFO)
            # file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # file_handler.setFormatter(file_formatter)
            # self.logger.addHandler(file_handler)

            # Add console handler to the logger
            self.logger.addHandler(console_handler)

        # Mark as initialized
        self._initialized = True

    def info(self, message: str, params: Optional[Dict] = None):
        """
        Log an info level message.
        """
        if params:
            self.logger.info(f"{message} | Params: {params}")
        else:
            self.logger.info(message)

    def warning(self, message: str, params: Optional[Dict] = None):
        """
        Log a warning level message.
        """
        if params:
            self.logger.warning(f"{message} | Params: {params}")
        else:
            self.logger.warning(message)

    def error(self, message: str, params: Optional[Dict] = None):
        """
        Log an error level message.
        """
        if params:
            self.logger.error(f"{message} | Params: {params}")
        else:
            self.logger.error(message)
