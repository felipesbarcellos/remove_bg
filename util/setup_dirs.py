import os

from loguru import logger
from util.constants import PATH_INPUT, PATH_OUTPUT, PATH_ORIGINALS

def setup_directories():
    directories = [PATH_INPUT, PATH_OUTPUT, PATH_ORIGINALS]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Directory {directory} is ready")
