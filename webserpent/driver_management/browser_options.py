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

    ACCEPT = "accept"
    DISMISS = "dismiss"
    IGNORE = "ignore"
    DISMISS_NOTIFY = "dismiss and notify"
    ACCEPT_NOTIFY = "accept and notify"


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

    def get(self) -> Union[ChromeOptions, FirefoxOptions, SafariOptions]:
        """return the webdriver options

        Returns:
            Union[ChromeOptions, FirefoxOptions, SafariOptions]
        """
        return self._options

    def make_headless(self):
        """Runs the browser without a UI, useful for running
        tests on servers or CI pipelines without a display.
        Feature is not available for Safari

        Browsers:
            Chrome, Firefox
        """
        if isinstance(self._options, SafariOptions):
            pass
        else:
            self._options.add_argument("--headless")

    def set_window_size(self, size: Union[Dict[str, int], str]):
        """Sets the browser to open at a specific resolution.

        Args:
            size (Union[Dict[str, int], str])

        Raises:
            TypeError: for having a dictionary with the wrong keys

        Browsers:
            Chrome, Firefox, Safari
        """
        if isinstance(size, dict):
            if "width" not in size or "height" not in size or len(size) != 2:
                raise TypeError(
                    "Expected a dict with exactly two keys: 'width' and 'height'"
                )
            if isinstance(self._options, (ChromeOptions, SafariOptions)):
                self._options.add_argument(
                    f"--window-size={size['width']},{size['height']}"
                )
            else:
                self._options.add_argument(f'--width={size['width']}')
                self._options.add_argument(f'--height={size['height']}')
            return

        raise TypeError("Expected a dict with keys 'width' and 'height'")

    def set_unhandled_alerts(self, option: UnhandledAlertChoice):
        """Defines the behavior when an unexpected alert appears during test execution.

        Args:
            option (UnhandledAlertChoice)

        Browsers:
            Chrome, Firefox, Safari
        """
        self._options.unhandled_prompt_behavior = option.value

    def set_ignore_ssl_errors(self):
        """turns on the ignore ssl error option

        Browsers:
            Chrome, Firefox
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_argument("--ignore-certificate-errors")
        elif isinstance(self._options, FirefoxOptions):
            self._options.set_preference(
                "network.proxy.allow_hijacking_localhost", True
            )

    def set_disabling_notifications(self):
        """Prevents pop-ups, such as location or notification requests, from interfering with tests.

        Browsers:
            Chrome, Firefox
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_experimental_option(
                "prefs", {"profile.default_content_setting_values.notifications": 2}
            )
        elif isinstance(self._options, FirefoxOptions):
            self._options.set_preference("dom.webnotifications.enabled", False)

    def disable_gpu_acceleration(self):
        """Disables GPU-based rendering for environments where it might cause issues.

        Browsers:
            Chrome
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_argument("--disable-gpu")

    def disable_extensions(self):
        """Ensures a clean browser state by disabling any pre-installed extensions.

        Browsers:
            Chrome, Firefox, Safari
        """
        self._options.add_argument("--disable-extensions")

    def set_emulate_mobile_device(self, device_name: str):
        """Configures the browser to mimic a mobile device for responsive design testing.

        Args:
            device_name (str)

        Browsers:
            Chrome
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_experimental_option(
                "mobileEmulation", {"deviceName": device_name}
            )

    def set_logging_preference(self, log_lvl: int):
        """Configures the level of browser logs (e.g., `INFO`, `DEBUG`, `OFF`).

        Args:
            log_lvl (int)

        Browsers:
            Chrome
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_argument(f"--log-level={log_lvl}")

    def disable_infobars(self):
        """Prevents "Chrome is being controlled by automated test software" messages.

        Browsers:
            Chrome
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_argument("--disable-infobars")

    def enable_experimental_webdriver_features(self):
        """Opt-in to new WebDriver capabilities or experimental browser features.

        Browsers:
            Chrome
        """
        if isinstance(self._options, ChromeOptions):
            self._options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )

    def _set_options(self, browser_choice: BrowserChoice):
        match browser_choice:
            case BrowserChoice.CHROME:
                self._options = ChromeOptions()
            case BrowserChoice.FIREFOX:
                self._options = FirefoxOptions()
            case BrowserChoice.SAFARI:
                self._options = SafariOptions()
