"""Module for driver wrapper"""

from typing import List, Tuple, Union

from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, NoSuchFrameException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from webserpent.configurations.configs import CONFIGS
from webserpent.logging.logger import get_system_logger, log_message
from webserpent.selenium.element import Element
from selenium.webdriver.remote.webelement import WebElement


logger = get_system_logger(__name__)


class Driver:
    def __init__(self, webdriver: WebDriver):
        self._driver = webdriver

    @property
    def current_url(self) -> str:
        """returns current page url

        Returns:
            str
        """
        logger.info("retrieving current url")
        url = self._driver.current_url
        logger.debug('current url is "%s"', url)
        return url

    @property
    def title(self) -> str:
        """returns current page title

        Returns:
            str
        """
        logger.info("retreiving page title")
        title = self._driver.title
        logger.debug('page title is "%s"', title)
        return title

    @property
    def window_handles(self) -> List[str]:
        """returns a list of window handle strs

        Returns:
            List[str]
        """
        logger.info("retrieving window handles")
        handles = self._driver.window_handles
        logger.debug("window handles are: %s", handles)
        return handles

    @property
    def current_window_handle(self) -> str:
        """returns current window handle str

        Returns:
            str
        """
        logger.info('retrieving current window handle')
        handle = self._driver.current_window_handle
        logger.debug('current window handle: %s', handle)
        return handle

    def find_element(
        self,
        locator: Tuple[By, str],
    ) -> WebElement:
        """returns a webelement

        Args:
            locator (Tuple[By, str])

        Returns:
            WebElement
        """
        by, location = locator
        logger.info('finding webelement with: (%s, %s)', by, location)
        try:
            element = self._driver.find_element(by, location)
            logger.debug('found element: %s', element.id)
            return element
        except NoSuchElementException as e:
            logger.debug('Element does not exist: (%s, %s)', by, location)
            logger.error('Error finding element: %s', e)
            raise

    def find_elements(
        self,
        locator: Tuple[By, str],
    ) -> List[WebElement]:
        """returns elements

        Args:
            locator (Tuple[By, str])

        Returns:
            List[WebElement]
        """
        by, location = locator
        logger.info('finding webelements with: (%s, %s)', by, location)
        try:
            elements = self._driver.find_elements(by, location)
            logger.debug('found elements: %s', elements)
            return elements
        except NoSuchElementException as e:
            logger.debug('Elements do not exist: (%s, %s)', by, location)
            logger.error('Error finding elements: %s', e)
            raise
        
    def switch_to_window(self, handle: str):
        """switch to window with given handle

        Args:
            handle (str)
        """
        logger.info('switching to window: %s', handle)
        try:
            self._driver.switch_to.window(handle)
        except NoSuchWindowException as e:
            logger.debug("window doesn't exist: %s", handle)
            logger.error('Error swithing to window: %s', e)
            raise
    
    def switch_to_frame(self, frame: Union[Tuple[By, str], WebElement, int]):
        """switch to a given frame

        Args:
            frame (Union[Tuple[By, str], WebElement, int])
        """
        logger.info('switching to frame: %s', frame)
        try:
            self._driver.switch_to.frame(frame)
        except NoSuchFrameException as e:
            logger.debug('No frame: %s', frame)
            logger.error('Error switching to frame: %s', e)
            raise
        

    def take_screenshot(self, file_path: str):
        """take a screen with at the given path

        Args:
            file_path (str)
        """
        logger.info('taking screenshot: %s', file_path)
        try:
            self._driver.save_screenshot(file_path)
        except WebDriverException as e:
            logger.debug('screenshot not saved to: %s', file_path)
            logger.error('Error saving screenshot: %s', e)
            raise
    
    def refresh(self):
        """refresh page
        """
        logger.info('refrshing driver')
        self._driver.refresh()

    def quit(self):
        """close down driver
        """
        logger.info('quitting driver')
        self._driver.quit()
