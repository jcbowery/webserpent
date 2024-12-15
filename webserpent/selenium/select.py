"""Module for select wrapping"""

from typing import List

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select as SeleniumSelect

from webserpent.logging.logger import get_system_logger

logger = get_system_logger(__name__)

class Select:
    """select wrapper"""
    def __init__(self, select: SeleniumSelect):
        self._select = select

    @property
    def options(self) -> List[WebElement]:
        """Returns all options in the select element."""
        logger.info("Getting all options from the select element")
        options = self._select.options
        logger.debug("Options retrieved: %s", [option.text for option in options])
        return options

    @property
    def all_selected_options(self):
        """Returns all selected options in the select element."""
        logger.info("Getting all selected options")
        selected_options = self._select.all_selected_options
        logger.debug("Selected options: %s", [option.text for option in selected_options])
        return selected_options

    @property
    def first_selected_option(self):
        """Returns the first selected option in the select element."""
        logger.info("Getting the first selected option")
        first_option = self._select.first_selected_option
        logger.debug("First selected option: %s", first_option.text)
        return first_option

    def select_by_value(self, value: str):
        """Selects an option by its value."""
        logger.info("Selecting option by value: %s", value)
        try:
            self._select.select_by_value(value)
            logger.debug("Option with value '%s' selected", value)
        except Exception as e:
            logger.error("Failed to select option by value '%s': %s", value, e)
            raise

    def select_by_visible_text(self, text: str):
        """Selects an option by its visible text."""
        logger.info("Selecting option by visible text: %s", text)
        try:
            self._select.select_by_visible_text(text)
            logger.debug("Option with visible text '%s' selected", text)
        except Exception as e:
            logger.error("Failed to select option by visible text '%s': %s", text, e)
            raise

    def select_by_index(self, index: int):
        """Selects an option by its index."""
        logger.info("Selecting option by index: %d", index)
        try:
            self._select.select_by_index(index)
            logger.debug("Option at index '%d' selected", index)
        except Exception as e:
            logger.error("Failed to select option by index '%d': %s", index, e)
            raise

    def deselect_all(self):
        """Deselects all options (only for multi-select)."""
        logger.info("Deselecting all options")
        try:
            self._select.deselect_all()
            logger.debug("All options deselected")
        except Exception as e:
            logger.error("Failed to deselect all options: %s", e)
            raise

    def deselect_by_value(self, value: str):
        """Deselects an option by its value."""
        logger.info("Deselecting option by value: %s", value)
        try:
            self._select.deselect_by_value(value)
            logger.debug("Option with value '%s' deselected", value)
        except Exception as e:
            logger.error("Failed to deselect option by value '%s': %s", value, e)
            raise

    def deselect_by_visible_text(self, text: str):
        """Deselects an option by its visible text."""
        logger.info("Deselecting option by visible text: %s", text)
        try:
            self._select.deselect_by_visible_text(text)
            logger.debug("Option with visible text '%s' deselected", text)
        except Exception as e:
            logger.error("Failed to deselect option by visible text '%s': %s", text, e)
            raise

    def deselect_by_index(self, index: int):
        """Deselects an option by its index."""
        logger.info("Deselecting option by index: %d", index)
        try:
            self._select.deselect_by_index(index)
            logger.debug("Option at index '%d' deselected", index)
        except Exception as e:
            logger.error("Failed to deselect option by index '%d': %s", index, e)
            raise
