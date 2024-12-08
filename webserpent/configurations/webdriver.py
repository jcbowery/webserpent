"""Module for webdriver configs"""

from dataclasses import dataclass
from webserpent.configurations.configs_base import ConfigBase

@dataclass
class WebDriverConfigs(ConfigBase):
    """Webdriver configurations"""
    headless: bool = True