"""Module for Element Class"""

from selenium.webdriver.remote.webelement import WebElement
from webserpent.logging.logger import get_system_logger

logger = get_system_logger(__name__)

class Element:
    """WebElement Wrapper"""

    def __init__(self, web_element: WebElement):
        self._element = web_element

    @property
    def text(self) -> str:
        """Returns the text of the web element."""
        logger.info("Retrieving text from the element")
        text = self._element.text
        logger.debug('Element text: "%s"', text)
        return text

    @property
    def is_displayed(self) -> bool:
        """Checks if the web element is displayed."""
        logger.info("Checking if element is displayed")
        displayed = self._element.is_displayed()
        logger.debug("Element displayed: %s", displayed)
        return displayed

    @property
    def is_enabled(self) -> bool:
        """Checks if the web element is enabled."""
        logger.info("Checking if element is enabled")
        enabled = self._element.is_enabled()
        logger.debug("Element enabled: %s", enabled)
        return enabled

    @property
    def is_selected(self) -> bool:
        """Checks if the web element is selected."""
        logger.info("Checking if element is selected")
        selected = self._element.is_selected()
        logger.debug("Element selected: %s", selected)
        return selected

    def click(self):
        """Click on the web element."""
        logger.info("Clicking on the element")
        try:
            self._element.click()
        except Exception as e:
            logger.error("Error clicking on the element: %s", e)
            raise

    def send_keys(self, text: str):
        """Send text to the web element."""
        logger.info('Sending "%s" to the element', text)
        try:
            self._element.send_keys(text)
        except Exception as e:
            logger.error('Error sending "%s" to the element: %s', text, e)
            raise

    def clear(self):
        """Clear the text from the web element."""
        logger.info("Clearing text from the element")
        self._element.clear()

    def get_attribute(self, attribute: str) -> str:
        """Get the value of an attribute from the web element."""
        logger.info('Getting attribute "%s" from the element', attribute)
        value = self._element.get_attribute(attribute)
        logger.debug('Element attribute "%s": %s', attribute, value)
        return value

    def get_css_value(self, value: str) -> str:
        """Get a CSS property value from the web element."""
        logger.info('Getting CSS property "%s" from the element', value)
        css_value = self._element.value_of_css_property(value)
        logger.debug('Element CSS value "%s": %s', value, css_value)
        return css_value
