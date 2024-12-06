"""Module for config classes"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Dict, Any

import toml

from webserpent.logging.logger import get_system_logger

logger = get_system_logger(__name__)


@dataclass
class Timeouts:
    """Time out configs"""

    implicit: int = None
    page_load: int = 10
    find_element: int = 5
    element_interaction: int = 2

    def validate(self):
        """validate if config values from toml file are correct type"""

        if not isinstance(self.implicit, Union[int, None]):
            raise TypeError(
                f"expected 'implicit' to be an int, got {type(self.implicit)}"
            )
        if not isinstance(self.page_load, int):
            raise TypeError(
                f"expected 'page_load' to be an int, got {type(self.page_load)}"
            )
        if not isinstance(self.find_element, int):
            raise TypeError(
                f"expected 'find_element' to be an int, got {type(self.find_element)}"
            )
        if not isinstance(self.element_interaction, int):
            raise TypeError(
                f"expected 'element_interact' to be an int, got {type(self.element_interaction)}"
            )


@dataclass
class WebDriverConfigs:
    """webdriver configs"""

    headless: bool = True
    timeouts: Timeouts = field(default_factory=Timeouts)

    def validate(self):
        """validate if config values from toml file are correct type"""
        if not isinstance(self.headless, bool):
            raise TypeError(
                f"expected 'headless' to be a bool, got {type(self.headless)}"
            )


def set_configs() -> WebDriverConfigs:
    """create figurations from toml file"""
    path = Path("webserpent.toml")
    if path.exists():
        toml_dict = _serialize_toml(path.name)
        webdriver_configs = _set_webdriverconfigs(toml_dict)
        return webdriver_configs
    logger.debug("no webserpent.toml config file found")
    logger.warning("using default configurations")
    return WebDriverConfigs()

def _serialize_toml(path: str) -> Dict[str, Any]:
    logger.info('serializing \'webserpent.toml\'')
    try:
        toml_dict = toml.load(path)
    except Exception as e:
        logger.critical('Error serializing file: %s', e)
        raise
    logger.debug("loaded config values:\n\t%s", toml_dict)
    return toml_dict


def _set_timeouts(toml_dict: dict) -> Timeouts:
    logger.info('checking for \'webdriver.timeouts\'')
    timeouts = toml_dict.get('webdriver', {}).get('timeouts', Timeouts())
    if isinstance(timeouts, dict):
        try:
            timeouts = Timeouts(**timeouts)
        except TypeError as e:
            logger.critical('Error serializing \'webdriver.timeouts\': %s', e)
            raise
    logger.debug(timeouts)
    return timeouts


def _set_webdriverconfigs(toml_dict) -> WebDriverConfigs:
    timeouts = _set_timeouts(toml_dict)
    logger.info('setting \'WebDriverConfigs\'')
    webdriver_configs = WebDriverConfigs(
        headless=toml_dict.get("webdriver", {}).get("headless", True), timeouts=timeouts
    )
    return webdriver_configs


CONFIGS = set_configs()
