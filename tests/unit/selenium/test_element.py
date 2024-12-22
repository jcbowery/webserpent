from webserpent.selenium.element import Element
from selenium.webdriver.remote.webelement import WebElement

def test_element_init(mocker):
    webelement_mock = mocker.Mock(spec='WebElement')
    element_name = 'test elmeent name'
    element = Element(webelement_mock, element_name)

    assert element._element == webelement_mock
    assert element._name == element_name