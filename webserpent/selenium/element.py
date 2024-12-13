"""Module for Element Class"""

from typing import Tuple, Optional
import logging
from logging import Logger

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from webserpent.configurations.configs import CONFIGS
from webserpent.logging.logger import get_system_logger, log_message
from webserpent.selenium.wait import Wait, is_true

logger = get_system_logger(__name__)


class Element:
    def __init__(self, web_element: WebElement, name: str, test_logger: Logger):
        self._element = web_element
        self._name = name
        self._logger = test_logger

    @property
    def in_viewport(self) -> bool:
        """Returns if element is in viewport"""
        logger.debug("returning if (%s) is in viewport", self._name)
        # Use JavaScript to check if the element is in the viewport
        element_rect = self._element.parent.execute_script(
            """
            var rect = arguments[0].getBoundingClientRect();
            var viewWidth = window.innerWidth || document.documentElement.clientWidth;
            var viewHeight = window.innerHeight || document.documentElement.clientHeight;
            return {
                top: rect.top >= 0 && rect.top < viewHeight,
                bottom: rect.bottom <= viewHeight,
                left: rect.left >= 0 && rect.left < viewWidth,
                right: rect.right <= viewWidth
            };
        """,
            self._element,
        )

        # Return True if all four sides of the element are within the viewport
        return (
            element_rect["top"]
            and element_rect["bottom"]
            and element_rect["left"]
            and element_rect["right"]
        )

    @property
    def text(self) -> str:
        """text of web element

        Returns:
            str
        """
        log_message(
            [logger, self._logger], logging.INFO, f"Returning text from ({self._name})"
        )
        return self._element.text

    @property
    def is_displayed(self) -> bool:
        """chcks if webelement is displayed on page. Does not check for being in view port

        Returns:
            bool
        """
        log_message(
            [logger, self._logger],
            logging.INFO,
            f"Returning whether ({self._name}) is displayed",
        )
        return self._element.is_displayed

    @property
    def is_enabled(self) -> bool:
        """chekcs if webelment is enabled

        Returns:
            bool
        """
        log_message(
            [logger, self._logger],
            logging.INFO,
            f"Returning whether ({self._name}) is enabled",
        )
        return self._element.is_enabled

    @property
    def is_selected(self) -> bool:
        """checks if webelement is selected

        Returns:
            bool
        """
        log_message(
            [logger, self._logger],
            logging.INFO,
            f"Returning whether ({self._name}) is selected",
        )
        return self._element.is_selected

    def click(self, timeout: Optional[int] = CONFIGS.TIMEOUTS.element_interaction):
        """click on element. If intercept try js click and if not interactable try to scroll then click

        Args:
            timeout (Optional[int]): Defaults to CONFIGS.TIMEOUTS.element_interaction.
        """
        Wait(timeout).until(EC.element_to_be_clickable(self._element))
        log_message([logger, self._logger], logging.INFO, f"clicking on ({self._name})")
        try:
            self._element.click()
        except ElementClickInterceptedException:
            log_message(
                [logger, self._logger],
                logging.WARNING,
                f"click on ({self._name}) intercepted. Attempting a js click",
            )
            self._js_click()
        except ElementNotInteractableException:
            log_message(
                [logger, self._logger],
                logging.WARNING,
                f"({self._name}) not interactable. Scrolling to element to try again.",
            )
            self.scroll_to()
            self._element.click()
        except Exception as e:
            log_message(
                [logger, self._logger],
                logging.ERROR,
                f"unknown error clicking ({self._name}): {e}",
            )
            raise

    def send_keys(self, text: str):
        """Sends text to webelement

        Args:
            text (str)
        """
        log_message(
            [logger, self._logger], logging.INFO, f'sending "{text}" to ({self._name})'
        )
        try:
            self._element.send_keys(text)
        except Exception as e:
            log_message(
                [logger, self._logger],
                logging.ERROR,
                f'error sending "{text}" to ({self._name}): {e}',
            )
            raise

    def scroll_to(self):
        """scroll to an element and wait for it to be in viewport"""
        self._element.parent.execute_script(
            "arguments[0].scrollIntoView(true);", self._element
        )
        Wait().until(is_true(self.in_viewport))

    def force_click(self):
        """scrolls to an elment and uses a js click
        """
        log_message(
            [logger, self._logger],
            logging.INFO,
            f"scrolling to and clicking on ({self._name}) with js",
        )
        self.scroll_to()
        self._element.parent.execute_script("arguments[0].click();", self._element)

    def find_element(self, locator: Tuple[By, str], name: str) -> "Element":
        """Find an element from an element

        Args:
            locator (Tuple[By, str]): _description_
            name (str): _description_

        Raises:
            NoSuchElementException: _description_

        Returns:
            Element: _description_
        """
        log_message(
            [logger, self._logger],
            logging.INFO,
            f'searching for element with: {locator} from ({self._name})'
        )
        try:
            Wait().until(EC.presence_of_element_located(locator))
            element = self._element.find_element(locator)
            return Element(element, name, self._logger)
        except TimeoutException:
            log_message(
                [logger, self._logger],
                logging.ERROR,
                f"timed out looking for {self._name}"
            )
            raise NoSuchElementException

    def clear(self):
        """clear text from element
        """
        log_message(
            [logger, self._logger],
            logging.INFO,
            f"clearing ({self._name})"
        )
        self._element.clear()

    def get_attribute(self, attribute: str) -> str:
        """returns attribute from element

        Args:
            attribute (str)

        Returns:
            str
        """
        log_message(
            [logger, self._logger],
            logging.INFO,
            f'returning "{attribute}" attribute from ({self._name})'
        )
        return self._element.get_attribute(attribute)

    def get_css_value(self, value: str) -> str:
        """returns css property value

        Args:
            value (str)

        Returns:
            str
        """
        log_message(
            [logger, self._logger],
            logging.INFO,
            f'returning "{value}" css property value from ({self._name})'
        )
        return self._element.value_of_css_property(value)

    def _js_click(self):
        self._element.parent.execute_script("arguments[0].click();", self._element)

    def _click(self):
        self._element.click()
