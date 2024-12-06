"""Module to hold logging setup methods"""

import logging
import sys
from pathlib import Path
import os

TEST_FMT_STR = "%(asctime)s - %(levelname)s - %(message)s"
SYSTEM_FMT_STR = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_system_logger(name: str):
    """Returns the system logger if env var ENV is set to dev

    Args:
        name (str)

    Returns:
        logging.Logger
    """
    if os.getenv("ENV", "dev").lower() == "dev":
        return _setup_system_logger(name)
    else:
        return _blank_logger()


def _setup_system_logger(name: str):
    system_logger = logging.getLogger(name)
    system_logger.setLevel(logging.DEBUG)

    # standard output handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_formatter = logging.Formatter(SYSTEM_FMT_STR)
    stdout_handler.setFormatter(stdout_formatter)

    # error handler
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_formatter = logging.Formatter(SYSTEM_FMT_STR)
    stderr_handler.setFormatter(stderr_formatter)

    ## Add handlers to logger
    if not system_logger.handlers:
        system_logger.addHandler(stdout_handler)
        system_logger.addHandler(stderr_handler)

    return system_logger


def setup_test_logger(name: str, path: str, file_name: str):
    """returns a testcase logger

    Args:
        name (str)
        path (str): directory path
        file_name (str): name of log file

    Returns:
        logging.Logger
    """
    file_logger = logging.getLogger(name)
    file_logger.setLevel(logging.INFO)

    # create folder location
    log_path = Path(path)
    log_path.mkdir(exist_ok=True)

    # file handler
    test_log_path = path + "/" + file_name
    file_handler = logging.FileHandler(filename=test_log_path)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(TEST_FMT_STR)
    file_handler.setFormatter(file_formatter)

    ## Add handlers to logger
    if not file_logger.handlers:
        file_logger.addHandler(file_handler)

    return file_logger


def _blank_logger():
    logger = logging.getLogger()
    bh = logging.NullHandler()
    logger.addHandler(bh)
    return logger
