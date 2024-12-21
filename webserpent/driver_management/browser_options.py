"""Module for handling browser options"""

from enum import Enum

from typing import Dict, Union

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions

# TODO: ADD system logging


class BrowserChoice(Enum):
    """Browser choices enum"""

    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"

class UnhandledAlertChoice(Enum):
    """Unhandled prompt option choice enum"""
    ACCEPT='accept'
    DISMISS='dismiss'
    IGNORE='ignore'
    DISMISS_NOTIFY='dismiss and notify'
    ACCEPT_NOTIFY='accept and notify'

class BrowserOptions:
    """Builder class for creating Selenium WebDriver Options"""

    def __init__(self, browser_choice: BrowserChoice):
        """Class takes in a BrowserChoice enum and assigns an Options object based
        on the choice.

        Args:
            browser_choice (BrowserChoice)
        """
        self._options = None
        self._set_options(browser_choice)

    def _set_options(self, browser_choice: BrowserChoice):
        match browser_choice:
            case BrowserChoice.CHROME:
                self._options = ChromeOptions()
            case BrowserChoice.FIREFOX:
                self._options = FirefoxOptions()
            case BrowserChoice.SAFARI:
                self._options = SafariOptions()

    def make_headless(self):
        """Runs the browser without a UI, useful for running
        tests on servers or CI pipelines without a display.
        Feature is not available for Safari
        """
        if isinstance(self._options, SafariOptions):
            pass
        else:
            self._options.add_argument("--headless")

    def set_window_size(self, size: Union[Dict[str, int], str]):
        """Sets the browser to open maximized or at a specific resolution.

        Args:
            size (Union[Dict[str, int], str])

        Raises:
            TypeError: for having a dictionary with the wrong keys
            TypeError: not passing in a dictionary or 'maximized'
        """
        if isinstance(size, dict):
            if "width" not in size or "height" not in size or len(size) != 2:
                raise TypeError(
                    "Expected a dict with exactly two keys: 'width' and 'height'"
                )
            self._options.add_argument(
                f"--window-size={size['width']},{size['height']}"
            )
            return

        if size == "maximized":
            self._options.add_argument("--start-maximized")
            return

        raise TypeError(
            "Expected a dict with keys 'width' and 'height' or the string 'maximized'"
        )

    def set_unhandled_alerts(self, option: UnhandledAlertChoice):
        """Defines the behavior when an unexpected alert appears during test execution.

        Args:
            option (UnhandledAlertChoice)
        """
        self._options.unhandled_prompt_behavior = option.value

    def set_ignore_ssl_errors(self):
        """turns on the ignore ssl error option
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_argument("--ignore-certificate-errors")
        elif isinstance(self._options, FirefoxOptions):
            self._options.set_preference("network.proxy.allow_hijacking_localhost", True)

    def set_disabling_notifications(self):
        """Prevents pop-ups, such as location or notification requests, from interfering with tests.
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
        elif isinstance(self._options, FirefoxOptions):
            self._options.set_preference("dom.webnotifications.enabled", False)


    def disable_gpu_acceleration(self):
        """Disables GPU-based rendering for environments where it might cause issues.
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_argument('--disable-gpu')    