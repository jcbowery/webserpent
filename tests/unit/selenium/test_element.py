import pytest
from selenium.webdriver.remote.webelement import WebElement
from webserpent.selenium.element import Element
from unittest.mock import MagicMock

@pytest.fixture
def mock_element(mocker):
    """Fixture to mock a WebElement"""
    element = mocker.MagicMock(spec=WebElement)
    return Element(element)

@pytest.fixture(autouse=True)
def mock_system_logger(mocker):
    """Mock the system logger to prevent actual logging during tests"""
    yield mocker.patch('webserpent.selenium.element.logger')

def test_text(mock_element, mock_system_logger):
    """Test the text property"""
    mock_element._element.text = "Mock Text"
    
    result = mock_element.text
    
    mock_system_logger.info.assert_called_once_with("Retrieving text from the element")
    mock_system_logger.debug.assert_called_once_with('Element text: "%s"', "Mock Text")
    assert result == "Mock Text"

def test_is_displayed(mock_element, mock_system_logger):
    """Test the is_displayed property"""
    mock_element._element.is_displayed.return_value = True
    
    result = mock_element.is_displayed
    
    mock_system_logger.info.assert_called_once_with("Checking if element is displayed")
    mock_system_logger.debug.assert_called_once_with("Element displayed: %s", True)
    assert result is True

def test_is_enabled(mock_element, mock_system_logger):
    """Test the is_enabled property"""
    mock_element._element.is_enabled.return_value = False
    
    result = mock_element.is_enabled
    
    mock_system_logger.info.assert_called_once_with("Checking if element is enabled")
    mock_system_logger.debug.assert_called_once_with("Element enabled: %s", False)
    assert result is False

def test_is_selected(mock_element, mock_system_logger):
    """Test the is_selected property"""
    mock_element._element.is_selected.return_value = True
    
    result = mock_element.is_selected
    
    mock_system_logger.info.assert_called_once_with("Checking if element is selected")
    mock_system_logger.debug.assert_called_once_with("Element selected: %s", True)
    assert result is True

def test_click(mock_element, mock_system_logger):
    """Test the click method"""
    mock_element._element.click = MagicMock()
    
    mock_element.click()
    
    mock_system_logger.info.assert_called_once_with("Clicking on the element")
    mock_element._element.click.assert_called_once()

def test_send_keys(mock_element, mock_system_logger):
    """Test the send_keys method"""
    text = "Test input"
    mock_element._element.send_keys = MagicMock()
    
    mock_element.send_keys(text)
    
    mock_system_logger.info.assert_called_once_with('Sending "%s" to the element', text)
    mock_element._element.send_keys.assert_called_once_with(text)

def test_clear(mock_element, mock_system_logger):
    """Test the clear method"""
    mock_element._element.clear = MagicMock()
    
    mock_element.clear()
    
    mock_system_logger.info.assert_called_once_with("Clearing text from the element")
