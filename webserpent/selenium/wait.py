"""Module for holding wait fuctions"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def wait_for_element_to_be_clickable(web_element: WebElement, timeout: int):
    """wait for an element to be clickable

    Args:
        web_element (WebElement)
        timeout (int)
    """
    wait = WebDriverWait(web_element, timeout)
    wait.until(EC.element_to_be_clickable(web_element))

def wait_for_element_to_be_in_viewport(web_element: WebElement, timeout: int):
    """wait for an element to be in the viewport

    Args:
        web_element (WebElement)
        timeout (int)
    """
    wait = WebDriverWait(web_element, timeout)
    wait.until(_in_viewport(web_element))

def _in_viewport(web_element: WebElement):
    """Returns if element is in viewport"""
    def _predicate(web_element: WebElement):
        # Use JavaScript to check if the element is in the viewport
        element_rect = web_element.parent.execute_script(
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
            web_element,
        )

        # Return True if all four sides of the element are within the viewport
        is_true = (
            element_rect["top"]
            and element_rect["bottom"]
            and element_rect["left"]
            and element_rect["right"]
        )
        return is_true
    return _predicate
