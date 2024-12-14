"""Module for wait functions"""

from typing import Tuple

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webserpent.logging.logger import get_system_logger
from webserpent.selenium.driver import Driver

logger = get_system_logger(__name__)

def wait_for_element_visible(driver: Driver, locator: Tuple[By, str], timeout: int):
    """Wait for an element to be visible"""
    try:
        by, location = locator
        logger.info("waiting %s seconds for element at (%s, %s) to be visible", timeout, by, location)
        WebDriverWait(driver._driver, timeout).until(EC.visibility_of_element_located(locator))
    except TimeoutException as e:
        logger.error("Element with locator %s was not visible within %s seconds.", locator, timeout)
        raise TimeoutException(f"Element with locator {locator} was not visible within {timeout} seconds.") from e
    except WebDriverException as e:
        logger.error("An error occurred with WebDriver during the wait.")
        raise WebDriverException("An error occurred with WebDriver during the wait.") from e

def wait_for_element_clickable(driver: Driver, locator: Tuple[By, str], timeout: int):
    """wait for an element to be clickable"""
    try:
        by, location = locator
        logger.info("waiting %s seconds for element at (%s, %s) to be clickable", timeout, by, location)
        WebDriverWait(driver._driver, timeout).until(EC.element_to_be_clickable(locator))
    except TimeoutException as e:
        logger.error("Element with locator %s was not clickable within %s seconds.", locator, timeout)
        raise TimeoutException(f"Element with locator {locator} was not clickable within {timeout} seconds.") from e
    except WebDriverException as e:
        logger.error("An error occurred with WebDriver during the wait.")
        raise WebDriverException("An error occurred with WebDriver during the wait.") from e

def wait_for_element_invisible(driver: Driver, locator: Tuple[By, str], timeout: int):
    """wait for an element to be invisible

    Args:
        driver (Driver)
        locator (Tuple[By, str])
        timeout (int)

    Raises:
        TimeoutException
        WebDriverException
    """
    try:
        by, location = locator
        logger.info("waiting %s seconds for element at (%s, %s) to be invisible", timeout, by, location)
        WebDriverWait(driver._driver, timeout).until(EC.invisibility_of_element_located(locator))
    except TimeoutException as e:
        logger.error("Element with locator %s was still visible after %s seconds.", locator, timeout)
        raise TimeoutException(f"Element with locator {locator} was still visible after {timeout} seconds.") from e
    except WebDriverException as e:
        logger.error("An error occurred with WebDriver during the wait.")
        raise WebDriverException("An error occurred with WebDriver during the wait.") from e

def wait_for_text_in_element(driver: Driver, locator: Tuple[By, str], text: str, timeout: int):
    """wait for an element to have given text

    Args:
        driver (Driver)
        locator (Tuple[By, str])
        text (str)
        timeout (int)

    Raises:
        TimeoutException
        WebDriverException
    """
    try:
        by, location = locator
        logger.info("waiting %s seconds for text '%s' to be present in element at (%s, %s)", timeout, text, by, location)
        WebDriverWait(driver._driver, timeout).until(EC.text_to_be_present_in_element(locator, text))
    except TimeoutException as e:
        logger.error("Text '%s' was not present in the element with locator %s within %s seconds.", text, locator, timeout)
        raise TimeoutException(f"Text '{text}' was not present in the element with locator {locator} within {timeout} seconds.") from e
    except WebDriverException as e:
        logger.error("An error occurred with WebDriver during the wait.")
        raise WebDriverException("An error occurred with WebDriver during the wait.") from e
