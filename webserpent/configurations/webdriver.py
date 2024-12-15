"""Module for webdriver configs"""

from dataclasses import dataclass, field
from webserpent.configurations.configs_base import ConfigBase
from webserpent.enums import BrowserType


@dataclass
class WebDriverConfigs(ConfigBase):
    """Webdriver configurations"""

    browser_type: BrowserType = BrowserType.CHROME
    browser_version: str = ""
    headless: bool = True
    window_size: dict = field(default_factory=lambda: {"width": 1920, "height": 1080})
    maximized: bool = False
    extensions: str = ""
    preferences: str = ""
    experimental_options: str = ""
    logging_prefs: str = ""
    mobile_emulation: bool = False
