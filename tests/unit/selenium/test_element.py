"""element tests"""
from unittest.mock import Mock

import pytest
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

from webserpent.selenium.element import (
    ClickFailureException,
    Element,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    FlakyClickException,
    FlakySendTetxException,
    InvalidElementStateException,
    SendTextFailureException,
    UnexpectedClickException,
    SelectBy
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

def test_send_text_success(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    element_name = 'test element'
    text_to_send = 'test text'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    element = Element(mock_web_element, element_name)

    element.send_text(text_to_send)

    element._element.send_keys.assert_called_once_with(text_to_send)

def test_send_text_scroll_fallback(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mock_web_element.send_keys.side_effect = [ElementNotInteractableException, None]
    element_name = 'test element'
    text_to_send = 'test text'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport')
    mock_scroll_to = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    element = Element(mock_web_element, element_name)

    element.send_text(text_to_send)

    assert element._element.send_keys.call_count == 2
    mock_scroll_to.assert_called_once()

def test_send_text_js_send_text_fallback(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mock_web_element.send_keys.side_effect = [ElementNotInteractableException, ElementNotInteractableException]
    element_name = 'test element'
    text_to_send = 'test text'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport')
    mock_scroll_to = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    mock_js_send_text = mocker.patch('webserpent.selenium.element.Element.js_send_text')
    element = Element(mock_web_element, element_name)

    element.send_text(text_to_send)

    assert element._element.send_keys.call_count == 2
    mock_scroll_to.assert_called_once()
    mock_js_send_text.assert_called_once_with(text_to_send)

def test_send_text_force_is_false(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mock_web_element.send_keys.side_effect = [ElementNotInteractableException, ElementNotInteractableException]
    element_name = 'test element'
    text_to_send = 'test text'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport')
    mock_scroll_to = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    mock_js_send_text = mocker.patch('webserpent.selenium.element.Element.js_send_text')
    element = Element(mock_web_element, element_name)

    with pytest.raises(FlakySendTetxException):
        element.send_text(text_to_send, force=False)

    assert element._element.send_keys.call_count == 2
    mock_scroll_to.assert_called_once()
    mock_js_send_text.assert_not_called()

def test_send_text_force_is_false(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    mock_web_element.send_keys.side_effect = [InvalidElementStateException]
    element_name = 'test element'
    text_to_send = 'test text'
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_clickable')
    mocker.patch('webserpent.selenium.element.wait_for_element_to_be_in_viewport')
    mock_scroll_to = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    mock_js_send_text = mocker.patch('webserpent.selenium.element.Element.js_send_text')
    element = Element(mock_web_element, element_name)

    with pytest.raises(SendTextFailureException):
        element.send_text(text_to_send)

    assert element._element.send_keys.call_count == 1

def test_clear(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    element_name = 'test element'
    element = Element(mock_web_element, element_name)

    element.clear()

    element._element.clear.assert_called_once()

@pytest.mark.parametrize('select_by, value', [
    (SelectBy.INDEX, "my index"),
    (SelectBy.VALUE, 'my value'),
    (SelectBy.VISIBLE_TEXT, 'my visible text')
])
def test_select_option_success(mocker, select_by, value):
    mock_web_element = mocker.Mock(spec=WebElement)
    element_name = 'test element'
    mock_select_instance = mocker.Mock(spec=Select)
    mocker.patch(
        "webserpent.selenium.element.Select", return_value=mock_select_instance
    )

    element = Element(mock_web_element, element_name)

    element.select_from_dropdown_by(select_by, value)

    match select_by:
        case SelectBy.INDEX:
            mock_select_instance.select_by_index.assert_called_once_with(value)
        case SelectBy.VALUE:
            mock_select_instance.select_by_value.assert_called_once_with(value) 
        case SelectBy.VISIBLE_TEXT:
            mock_select_instance.select_by_visible_text.assert_called_once_with(value) 


@pytest.mark.parametrize('select_by, value', [
    (SelectBy.INDEX, "my index"),
    (SelectBy.VALUE, 'my value'),
    (SelectBy.VISIBLE_TEXT, 'my visible text')
])
def test_deselect_option_success(mocker, select_by, value):
    mock_web_element = mocker.Mock(spec=WebElement)
    element_name = 'test element'
    mock_select_instance = mocker.Mock(spec=Select)
    mocker.patch(
        "webserpent.selenium.element.Select", return_value=mock_select_instance
    )

    element = Element(mock_web_element, element_name)

    element.deselect_from_dropdown_by(select_by, value)

    match select_by:
        case SelectBy.INDEX:
            mock_select_instance.deselect_by_index.assert_called_once_with(value)
        case SelectBy.VALUE:
            mock_select_instance.deselect_by_value.assert_called_once_with(value) 
        case SelectBy.VISIBLE_TEXT:
            mock_select_instance.deselect_by_visible_text.assert_called_once_with(value) 


def test_deselect_all(mocker):
    mock_web_element = mocker.Mock(spec=WebElement)
    element_name = 'test element'
    mock_select_instance = mocker.Mock(spec=Select)
    mocker.patch(
        "webserpent.selenium.element.Select", return_value=mock_select_instance
    )

    element = Element(mock_web_element, element_name)

    element.deselect_all()

    mock_select_instance.deselect_all.assert_called_once()