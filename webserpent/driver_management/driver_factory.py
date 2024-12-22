"""Module for creating webdrivers"""

from typing import Union

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from webserpent.driver_management.browser_options import (
    ChromeOptions,
    FirefoxOptions,
    SafariOptions,
)

# TODO: ADD system logging


def get_local(browser_options: Union[ChromeOptions, FirefoxOptions, SafariOptions]) -> WebDriver:
    """get a local driver based on browser options type

    Args:
        browser_options (Union[ChromeOptions, FirefoxOptions, SafariOptions])

    Raises:
        TypeError: when non supported browser type passed

    Returns:
        WebDriver 
    """
    if isinstance(browser_options, ChromeOptions):
        return webdriver.Chrome(options=browser_options)
    if isinstance(browser_options, FirefoxOptions):
        return webdriver.Firefox(options=browser_options)
    if isinstance(browser_options, SafariOptions):
        return webdriver.Safari(options=browser_options)
    raise TypeError("Unsupported browser options provided.")
