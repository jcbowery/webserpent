from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from webserpent.selenium.wait import wait_for_element_to_exist, wait_for_alert
from webserpent.selenium.element import Element

# TODO: add configurations
# TODO: add logging

class page:
    def __init__(self, driver: WebDriver):
        self._driver = driver
        self.title = 'None Set'
        self.url = 'None Set'

    def find_element(self, locator: Tuple[By, str], name: str, timeout :int = 5) -> Element:
        wait_for_element_to_exist(self._driver, locator, timeout)

        element = self._driver.find_element(*locator)
        return Element(element, name)

    def dismiss_alert(self, timeout: int=5):
        alert = wait_for_alert(self._driver, timeout)
        alert.dismiss()

    def accept_confirmation(self, timeout: int = 5):
        alert = wait_for_alert(self._driver, timeout)
        alert.accept()

    def dismiss_confirmation(self, timeout: int = 5):
        alert = wait_for_alert(self._driver, timeout)
        alert.dismiss()

    def send_text_to_prompt(self, text:str, timeout: int = 5):
        alert = wait_for_alert(self._driver, timeout)
        alert.send_keys(text)

    def get_text_of_alert(self, timeout: int = 5):
        alert = wait_for_alert(self._driver, timeout)
        return alert.text
