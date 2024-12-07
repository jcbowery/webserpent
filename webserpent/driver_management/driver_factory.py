"""Module for the Driver Factor class"""

from logging import Logger
import logging
from typing import Union

from selenium import webdriver

from webserpent.driver_management.options_builder import (
    BrowserType,
    ChromeOptions,
    FirefoxOptions,
    SafariOptions,
)
from webserpent.logging.logger import get_system_logger, log_message

logger = get_system_logger(__name__)


class DriverFactory:
    """Class for generating drivers"""

    @staticmethod
    def get_local(
        test_logger: Logger,
        browser_type: BrowserType,
        options: Union[ChromeOptions, FirefoxOptions, SafariOptions] = None,
    ):
        """Returns a local driver instance

        Args:
            test_logger (Logger)

            browser_type (BrowserType)

            options (Union[ChromeOptions, FirefoxOptions, SafariOptions], optional): 
                Defaults to None.

        Raises:
            ValueError: Raises error if incorrect BrowserType is given

        Returns:
            WebDriver
        """
        log_message(
            [logger, test_logger],
            logging.DEBUG,
            f"Returning browser of type: {browser_type}",
        )
        match browser_type:
            case BrowserType.CHROME:
                logger.debug("returning chrome driver")
                return webdriver.Chrome(options=options)
            case BrowserType.FIREFOX:
                return webdriver.Firefox(options=options)
            case BrowserType.SAFARI:
                return webdriver.Safari(options=options)
            case _:
                raise ValueError(f"BrowserType {browser_type} not supported.")
