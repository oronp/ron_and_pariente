import os
from pathlib import Path
from dataclasses import dataclass


@dataclass
class BaseConfig:
    CONFIG_DIR_PATH: str = os.path.dirname(__file__)
    PROJECT_BASE_DIR_PATH: str = Path(CONFIG_DIR_PATH).parent
    FILES_DIR_PATH: str = os.path.join(PROJECT_BASE_DIR_PATH, 'files')
    DATE_TIME_FORMAT: str = '%d/%m/%Y, %H:%M:%S'  # e.g., '25/12/2021, 14:35'
    CHAT_FILE_NAME: str = 'chat.txt'
    CHAT_FILE_PATH: str = os.path.join(FILES_DIR_PATH, CHAT_FILE_NAME)

    PATTERN: str = r'^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}:\d{2})\]\s([^:]+):\s(.*)'
    WEIGHT_PATTERN: str = r'\b\d{2}\.\d\b'
