"""Module for options builder class"""

from typing import Union

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions

from webserpent.enums import BrowserType
from webserpent.logging.logger import get_system_logger

logger = get_system_logger(__name__)


class OptionsBuilder:
    """Builder class to build WebDriver Options"""

    def __init__(self, browser_type: BrowserType):
        logger.debug("OptionsBuilder initialized with browser_type: %s", browser_type)
        self.options: Union[ChromeOptions, FirefoxOptions, SafariOptions] = None
        match browser_type:
            case BrowserType.CHROME:
                self.options = ChromeOptions()
            case BrowserType.FIREFOX:
                self.options = FirefoxOptions()
            case BrowserType.SAFARI:
                self.options = SafariOptions()
            case _:
                raise ValueError(f"Unsupported browser type: {browser_type.value}")

    def get(self) -> Union[ChromeOptions, FirefoxOptions, SafariOptions]:
        """Get driver options"""
        logger.debug("Returning options object")
        return self.options

    def set_browser_version(self, version: str):
        """Set the available browser version at remote end

        Args:
            version (str): Browser version
        """
        logger.debug("Setting browser version to %s", version)
        if hasattr(self.options, "browser_version"):
            self.options.browser_version = version
        else:
            logger.warning("Browser version setting is not supported for this browser type")
        return self

    def set_page_load_timeout(self, time: int):
        """Set the page load timeout.

        Args:
            time (int): Time in milliseconds
        """
        logger.debug("Setting page load timeout: %s", time)
        if hasattr(self.options, "timeouts"):
            self.options.timeouts = {'pageLoad': time}
        return self

    def set_implicit_wait_timeout(self, time: int):
        """Set the implicit wait timeout.

        Args:
            time (int): Time in milliseconds
        """
        logger.debug("Setting implicit wait timeout: %s", time)
        if hasattr(self.options, "timeouts"):
            self.options.timeouts["implicit"] = time
        return self

    def headless(self):
        """Set driver to headless mode"""
        logger.debug("Setting driver to headless mode")
        if isinstance(self.options, (ChromeOptions, FirefoxOptions)):
            self.options.add_argument("--headless")
        if isinstance(self.options, ChromeOptions):
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
        return self

    def set_window_size(self, width: int, height: int):
        """Set the browser window size.

        Args:
            width (int): Window width
            height (int): Window height
        """
        logger.debug("Setting window size to %sx%s", width, height)
        self.options.add_argument(f"--window-size={width},{height}")
        return self

    def set_binary_location(self, path: str):
        """Set the path to the browser binary.

        Args:
            path (str): Path to the browser binary
        """
        logger.debug("Setting binary location to %s", path)
        self.options.binary_location = path
        return self

    def add_extension(self, path: str):
        """Add a browser extension.

        Args:
            path (str): Path to the extension file
        """
        logger.debug("Adding extension: %s", path)
        self.options.add_extension(path)
        return self

    def set_preferences(self, prefs: dict):
        """Set browser preferences.

        Args:
            prefs (dict): Dictionary of preferences
        """
        logger.debug("Setting preferences: %s", prefs)
        if isinstance(self.options, ChromeOptions):
            self.options.add_experimental_option("prefs", prefs)
        if isinstance(self.options, FirefoxOptions):
            for key, value in prefs.items():
                self.options.set_preference(key, value)
        return self

    def set_experimental_option(self, name: str, value):
        """Set an experimental option.

        Args:
            name (str): Name of the option
            value: Value of the option
        """
        logger.debug("Setting experimental option %s to %s", name, value)
        if isinstance(self.options, ChromeOptions):
            self.options.add_experimental_option(name, value)
        return self

    def set_capability(self, name: str, value):
        """Set a capability.

        Args:
            name (str): Name of the capability
            value: Value of the capability
        """
        logger.debug("Setting capability %s to %s", name, value)
        self.options.set_capability(name, value)
        return self

    def set_unhandled_alert_behavior(self, behavior: str):
        """Set the behavior for unhandled alerts.

        Args:
            behavior (str): One of 'accept', 'dismiss', or 'ignore'.
        """
        logger.debug("Setting unhandled alert behavior to %s", behavior)
        self.options.set_capability("unhandledPromptBehavior", behavior)
        return self

    def enable_logging_prefs(self, logging_prefs: dict):
        """Enable logging preferences for the browser.

        Args:
            logging_prefs (dict): Logging preferences dictionary
        """
        logger.debug("Setting logging preferences: %s", logging_prefs)
        if isinstance(self.options, ChromeOptions):
            self.options.set_capability("goog:loggingPrefs", logging_prefs)
        return self

    def enable_mobile_emulation(self, device_name: str):
        """Enable mobile emulation mode for Chrome.

        Args:
            device_name (str): Name of the device to emulate
        """
        logger.debug("Enabling mobile emulation for device: %s", device_name)
        if isinstance(self.options, ChromeOptions):
            self.options.add_experimental_option("mobileEmulation", {"deviceName": device_name})
        return self
