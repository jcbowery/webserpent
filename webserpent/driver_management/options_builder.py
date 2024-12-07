"""Module for options builder class"""

from logging import Logger
import logging
from typing import Union

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions

from webserpent.enums import BrowserType
from webserpent.logging.logger import get_system_logger, log_message

logger = get_system_logger(__name__)


class OptionsBuilder:
    """Builder class to build WebDriver Options"""

    def __init__(self, browser_type: BrowserType, test_logger: Logger):
        self.test_logger = test_logger
        log_message(
            [logger, self.test_logger],
            logging.DEBUG,
            f"'OptionsBuilder initialized with 'browser_type: {browser_type}",
        )
        self.options: Union[ChromeOptions, FirefoxOptions, SafariOptions] = None
        match browser_type:
            case BrowserType.CHROME:
                self.options = ChromeOptions()
            case BrowserType.FIREFOX:
                self.options = FirefoxOptions()
            case BrowserType.SAFARI:
                self.options = SafariOptions()
            case _:
                raise ValueError(f"Unsupported browser type: {browser_type}")

    def get(self) -> Union[ChromeOptions, FirefoxOptions, SafariOptions]:
        """get driver options"""
        log_message(
            [logger, self.test_logger],
            logging.DEBUG,
            "returning options object",
        )
        return self.options

    def set_browser_version(self, version: str):
        """set the available browser version at remote end

        Args:
            version (str): browser version
        """
        log_message(
            [logger, self.test_logger],
            logging.DEBUG,
            f"setting browser version to {version}",
        )
        self.options.browser_version = version
        return self

    def set_page_load_timeout(self, time: int):
        """Specifies the time interval in which web page needs to be 
        loaded in a current browsing context.
        The default timeout 300,000 is imposed when a new session 
        is created by WebDriver. If page load limits a given/default time frame, 
        the script will be stopped by TimeoutException.

        Args:
            time (int): time in millseconds
        """
        log_message(
            [logger, self.test_logger],
            logging.DEBUG,
            f"setting page load timeout: {time}",
        )
        self.options.timeouts = {"pageLoad": time * 1000}
        return self

    def set_implicit_wait_timout(self, time: int):
        """This specifies the time to wait for the implicit 
        element location strategy when locating elements.
        The default timeout 0 is imposed when a new session is created by WebDriver.

        Args:
            time (int): millseconds
        """
        log_message(
            [logger, self.test_logger], logging.DEBUG, f"setting implicit wait: {time}"
        )
        self.options.timeouts = {"implicit": time}
        return self

    def headless(self):
        """sets driver to headless mode"""
        log_message(
            [logger, self.test_logger], logging.DEBUG, "setting driver to headless"
        )
        if isinstance(self.options, (FirefoxOptions, SafariOptions)):
            self.options.add_argument("--headless")
        if isinstance(self.options, ChromeOptions):
            self.options.add_argument("--headless")  # Enable headless mode
            self.options.add_argument(
                "--disable-gpu"
            )  # Disable GPU acceleration (optional)
            self.options.add_argument("--no-sandbox")  # Disable sandboxing (optional)

        return self
