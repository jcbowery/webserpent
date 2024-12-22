from selenium.webdriver.remote.webelement import WebElement

class Element:
    def __init__(self, web_element: WebElement, name: str):
        self._element = web_element
        self._name = name