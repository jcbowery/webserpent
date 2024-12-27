"""Module for holding selenium element wrappings"""

from enum import Enum

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidElementStateException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from webserpent.exceptions.exceptions import (
    ClickFailureException,
    FlakyClickException,
    UnexpectedClickException,
    FlakySendTetxException,
    SendTextFailureException,
    UnexptedSendTextException,
    SelectFailureException,
    FlakySelectException,
    UnexpectedSelectException,
)
from webserpent.selenium.wait import (
    wait_for_element_to_be_clickable,
    wait_for_element_to_be_in_viewport,
)

# TODO: Add test logger
# TODO: Add configuration values


class SelectBy(Enum):
    INDEX = "index"
    VALUE = "value"
    VISIBLE_TEXT = "visible_text"


class Element:
    """Class tow rap selenium WebElement"""

    def __init__(self, web_element: WebElement, name: str):
        self._element = web_element
        self._name = name

    @property
    def tag_name(self) -> str:
        """Get element tag name

        Returns:
            str
        """
        return self._element.tag_name

    @property
    def text(self) -> str:
        """Get element text

        Returns:
            str
        """
        return self._element.text

    @property
    def id(self) -> str:
        """Get element id

        Returns:
            str:
        """
        return self._element.id

    @property
    def size(self) -> dict:
        """Get element size.

        Returns:
            dict: {'width': <int>, 'height': <int>}
        """
        return self._element.size

    @property
    def location(self) -> dict:
        """Return element location

        Returns:
            dict:
        """
        return self._element.location

    @property
    def rect(self) -> dict:
        """A dictionary with the size and location of the element.

        Returns:
            dict
        """
        return self._element.rect

    @property
    def enabled(self) -> bool:
        """Returns if an element is enabled

        Returns:
            bool:
        """
        return self._element.is_enabled()

    @property
    def selected(self) -> bool:
        """Return if element is selected

        Returns:
            bool: 
        """
        return self._element.is_selected()

    @property
    def displayed(self) -> bool:
        """Return if element is displayed on the DOM

        Returns:
            bool: 
        """
        return self._element.is_displayed()

    @property
    def in_viewport(self) -> bool:
        """Returns if element is in viewport"""
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
        is_true = (
            element_rect["top"]
            and element_rect["bottom"]
            and element_rect["left"]
            and element_rect["right"]
        )
        return is_true

    def get_attribute(self, name: str) -> str:
        """Get a given attribute value

        Args:
            name (str):

        Returns:
            str:
        """
        return self._element.get_attribute(name)

    def get_property(self, name: str) -> str:
        """Get given property value

        Args:
            name (str):

        Returns:
            str: 
        """
        return self._element.get_property(name)

    def click(self, timeout: int = 5, force: bool = True):
        """Click the element. If ElementClickInterceptedException or
        ElementNotInteractableException is raised a scroll to element action is performed
        and a second click attempt is made. With force = True, if the second attempt also
        raises one of thsoe errors a js click is performed.

        Args:
            timeout (int, optional): Defaults to 5.
            force (bool, optional): Defaults to True.

        Raises:
            ClickFailureException:
            FlakyClickException:
            UnexpectedClickException:
        """
        try:
            wait_for_element_to_be_clickable(self._element, timeout)
        except TimeoutException as e:
            raise ClickFailureException(
                "Failure to click on {self._name} due to timeout"
            ) from e

        attempts = 1
        while attempts <= 2:
            try:
                self._element.click()
                break
            except (
                ElementClickInterceptedException,
                ElementNotInteractableException,
            ) as e:
                if attempts == 1:
                    self.scroll_to()
                    attempts += 1
                else:
                    if force:
                        self.js_click()
                        break
                    raise FlakyClickException(
                        f"Issues with clicking {self._name}"
                    ) from e
            except StaleElementReferenceException:
                raise
            except InvalidElementStateException as e:
                raise ClickFailureException(f"Failure to click on {self._name}") from e
            except Exception as e:
                raise UnexpectedClickException("Unknown Error") from e

    def send_text(self, text: str, timeout: int = 3, force=True):
        """send text to an element. If ElementClickInterceptedException or
        ElementNotInteractableException is raised a scroll to element action is performed
        and a second send text attempt is made. With force = True, if the second attempt also
        raises one of thsoe errors a js send text is performed.

        Args:
            text (str)
            timeout (int, optional):  Defaults to 3.
            force (bool, optional):  Defaults to True.

        Raises:
            SendTextFailureException:
            FlakySendTetxException:
            SendTextFailureException:
            UnexptedSendTextException:
        """
        try:
            wait_for_element_to_be_clickable(self._element, timeout)
        except TimeoutException as e:
            raise SendTextFailureException(
                "Failure to send text to {self._name} due to timeout"
            ) from e

        attempts = 1
        while attempts <= 2:
            try:
                self._element.send_keys(text)
                break
            except (
                ElementClickInterceptedException,
                ElementNotInteractableException,
            ) as e:
                if attempts == 1:
                    self.scroll_to()
                    attempts += 1
                else:
                    if force:
                        self.js_send_text(text)
                        break
                    raise FlakySendTetxException(
                        f"Issues with sending text to {self._name}"
                    ) from e
            except StaleElementReferenceException:
                raise
            except InvalidElementStateException as e:
                raise SendTextFailureException(
                    f"Failure to send text to {self._name}"
                ) from e
            except Exception as e:
                raise UnexptedSendTextException("Unknown Error") from e

    def clear(self):
        """Clear text from text field"""
        self._element.clear()

    def select_from_dropdown_by(self, select_by: SelectBy, value: str):
        """Select from a dropdown by type and value

        Args:
            select_by (SelectBy)
            value (str)

        Raises:
            FlakySelectException:
            SelectFailureException:
            UnexpectedSelectException:
        """
        select = Select(self._element)
        try:
            match select_by:
                case SelectBy.VALUE:
                    select.select_by_value(value)
                case SelectBy.INDEX:
                    select.select_by_index(value)
                case SelectBy.VISIBLE_TEXT:
                    select.select_by_visible_text(value)
        except (
            ElementNotInteractableException,
            StaleElementReferenceException,
            ElementClickInterceptedException,
        ) as e:
            raise FlakySelectException("Issue with selecting element") from e
        except InvalidElementStateException as e:
            raise SelectFailureException("Failure to select element") from e
        except Exception as e:
            raise UnexpectedSelectException("Unexpected error occured") from e

    def deselect_from_dropdown_by(self, select_by: SelectBy, value: str):
        """Deseelct from a dropdown by type and value

        Args:
            select_by (SelectBy)
            value (str)

        Raises:
            FlakySelectException:
            SelectFailureException:
            UnexpectedSelectException:
        """
        select = Select(self._element)
        try:
            match select_by:
                case SelectBy.VALUE:
                    select.deselect_by_value(value)
                case SelectBy.INDEX:
                    select.deselect_by_index(value)
                case SelectBy.VISIBLE_TEXT:
                    select.deselect_by_visible_text(value)
        except (
            ElementNotInteractableException,
            StaleElementReferenceException,
            ElementClickInterceptedException,
        ) as e:
            raise FlakySelectException("Issue with selecting element") from e
        except InvalidElementStateException as e:
            raise SelectFailureException("Failure to select element") from e
        except Exception as e:
            raise UnexpectedSelectException("Unexpected error occured") from e

    def deselect_all(self):
        """Deselect all items in dropdown

        Raises:
            FlakySelectException:
            SelectFailureException:
            UnexpectedSelectException:
        """
        select = Select(self._element)
        try:
            select.deselect_all()
        except (
            ElementNotInteractableException,
            StaleElementReferenceException,
            ElementClickInterceptedException,
        ) as e:
            raise FlakySelectException("Issue with selecting element") from e
        except InvalidElementStateException as e:
            raise SelectFailureException("Failure to select element") from e
        except Exception as e:
            raise UnexpectedSelectException("Unexpected error occured") from e

    def scroll_to(self, timeout=3):
        """Scroll to element and wait for it to be in viewport"""
        self._element.parent.execute_script(
            "arguments[0].scrollIntoView(true);", self._element
        )
        wait_for_element_to_be_in_viewport(self._element, timeout)

    def js_click(self):
        """click with js"""
        self._element.parent.execute_script("arguments[0].click();", self._element)

    def js_send_text(self, text: str):
        """send text via js"""
        js_code = """
        var input = arguments[0];
        var value = arguments[1];
        input.value = value;
        var event = new Event('input', { bubbles: true });
        input.dispatchEvent(event);
        """
        self._element.parent.execute_script(js_code, self._element, text)
