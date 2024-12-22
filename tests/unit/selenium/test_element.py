import pytest
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from webserpent.selenium.element import (
    ClickFailureException,
    Element,
    ElementClickInterceptedException,
    FlakyClickException,
    InvalidElementStateException,
    UnexpectedClickException,
)

@pytest.fixture
def element(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable', return_value = True)
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport', return_value = True)
    element_class = Element(mock_web_element, 'test element')
    
    yield element_class

def test_element_init(mocker):
    webelement_mock = mocker.Mock(spec=WebElement)
    element_name = 'test elmeent name'
    element = Element(webelement_mock, element_name)

    assert element._element == webelement_mock
    assert element._name == element_name

def test_click_performs_a_click(element):
    element.click()

    element._element.click.assert_called_once()


def test_click_scroll_and_retry(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mock_web_element.click.side_effect = [ElementClickInterceptedException, None]
    element_name = 'test element'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport')
    mock_scroll_to = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    element = Element(mock_web_element, element_name)

    element.click()

    mock_scroll_to.assert_called_once()
    assert mock_web_element.click.call_count == 2

def test_click_js_fallback(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mock_web_element.click.side_effect = [ElementClickInterceptedException, ElementClickInterceptedException]
    element_name = 'test element'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport')
    mock_scroll_to = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    mock_js_click = mocker.patch('webserpent.selenium.element.Element.js_click')
    element = Element(mock_web_element, element_name)

    element.click()

    mock_scroll_to.assert_called_once()
    mock_js_click.assert_called_once()
    assert mock_web_element.click.call_count == 2

def test_click_raises_flaky_click_exception(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mock_web_element.click.side_effect = [ElementClickInterceptedException, ElementClickInterceptedException]
    element_name = 'test element'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport')
    mock_scroll_to = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    mock_js_click = mocker.patch('webserpent.selenium.element.Element.js_click')
    element = Element(mock_web_element, element_name)

    with pytest.raises(FlakyClickException):
        element.click(force=False)
    assert mock_web_element.click.call_count == 2


def test_click_raises_click_failure_exception(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mock_web_element.click.side_effect = [InvalidElementStateException]
    element_name = 'test element'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport')
    mock_scroll_to = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    mock_js_click = mocker.patch('webserpent.selenium.element.Element.js_click')
    element = Element(mock_web_element, element_name)

    with pytest.raises(ClickFailureException):
        element.click()
    assert mock_web_element.click.call_count == 1


def test_click_raises_unexpected_click_exception(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mock_web_element.click.side_effect = [Exception]
    element_name = 'test element'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport')
    mock_scroll_to = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    mock_js_click = mocker.patch('webserpent.selenium.element.Element.js_click')
    element = Element(mock_web_element, element_name)

    with pytest.raises(UnexpectedClickException):
        element.click()
    assert mock_web_element.click.call_count == 1
    
