"""Module for handling browser options"""

from enum import Enum

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions

# TODO: ADD system logging


class BrowserChoice(Enum):
    """Browser choices enum"""
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"


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
