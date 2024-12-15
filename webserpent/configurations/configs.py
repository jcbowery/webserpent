"""Module for setting and holding configurations"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import toml

from webserpent.configurations.system import SystemConfigs
from webserpent.configurations.timeouts import TimeOuts
from webserpent.configurations.webdriver import WebDriverConfigs
from webserpent.logging.logger import get_system_logger
from webserpent.enums import string_to_enum, BrowserType

logger = get_system_logger(__name__)


class TOML:
    """toml wrapper class"""

    def __init__(self):
        self.toml = toml

    def load(self, path: str) -> dict:
        """takes a parth to a toml file to return a dict

        Args:
            path (str):

        Returns:
            dict:
        """
        return self.toml.load(path)


@dataclass
class Configs:
    """configurations data class to hold config values"""

    system: SystemConfigs
    timeouts: TimeOuts
    webdriver: WebDriverConfigs


def _set_configs():
    toml_dict = _create_toml_dict()
    # system configs
    system_configs = _create_config(toml_dict.get("system", {}), SystemConfigs)
    system_configs.validate()
    # timeouts
    timeout_configs = _create_config(toml_dict.get("timeouts", {}), TimeOuts)
    timeout_configs.validate()
    # webdriver configs
    browser_type_string = toml_dict.get("webdriver").get("browser_type")
    toml_dict.get("webdriver").update(
        {"browser_type": string_to_enum(browser_type_string, BrowserType)}
    )
    webdriver_configs = _create_config(toml_dict.get("webdriver", {}), WebDriverConfigs)
    webdriver_configs.validate()

    # output configurations
    return Configs(
        system=system_configs, timeouts=timeout_configs, webdriver=webdriver_configs
    )


def _create_toml_dict() -> dict:
    logger.info("Checking for configuration file")
    path = Path("webserpent.toml")
    if path.exists():
        logger.info("configuration file found, Setting values")
        toml_dict = _serialize_toml(path.name)
        logger.debug("configuration values: %s", toml_dict)
    else:
        logger.warning("'webserpent.toml' not found. Using default values")
        toml_dict = {}
    return toml_dict


def _create_config(toml_dict: dict, cls):
    try:
        return cls(**toml_dict)
    except TypeError as e:
        logger.critical(e)
        raise


def _serialize_toml(path: str) -> Dict[str, Any]:
    logger.info("serializing 'webserpent.toml'")
    try:
        toml_dict = TOML().load(path)
    except Exception as e:
        logger.critical("Error serializing file: %s", e)
        raise
    logger.debug("loaded config values:\n\t%s", toml_dict)
    return toml_dict


CONFIGS = _set_configs()
