from typing import Union

from selenium.webdriver.remote.webdriver import WebDriver

# TODO: add logging

class Browser:
    def __init__(self, driver: WebDriver):
        self._driver = driver

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    @property
    def current_title(self) -> str:
        return self._driver.title

    def refresh(self):
        self._driver.refresh()

    def back(self):
        self._driver.back()

    def forward(self):
        self._driver.forward()

    def navigate_to(self, url: str):
        self._driver.get(url)

    def take_screenshot(self, ss_type: str, path: str = '' ) -> Union[str, None]:
        """Saves a screen shot.

        Args:
            ss_type (str): 'base64' will return the base64 encoded string 
                and 'png' will save a png at given location
            path (str): 

        Returns:
            Union[str, None]:
        """
        match ss_type:
            case 'base64':
                return self._driver.get_screenshot_as_base64()
            case 'png':
                self._driver.get_screenshot_as_file(path)
