from unittest.mock import MagicMock

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from webserpent.selenium.wait import (
    wait_for_element_to_be_clickable,
    wait_for_element_to_be_in_viewport,
)

@pytest.fixture
def mock_web_element():
    return MagicMock(spec=WebElement)

@pytest.fixture
def mock_wait(mocker):
    return mocker.patch("webserpent.selenium.wait.WebDriverWait")

def test_wait_for_element_to_be_clickable(mock_wait, mock_web_element, mocker):
    # Arrange
    mock_wait_instance = mock_wait.return_value
    mock_wait_instance.until.return_value = None
    mock_ec = mocker.patch("selenium.webdriver.support.expected_conditions.element_to_be_clickable")

    # Act
    wait_for_element_to_be_clickable(mock_web_element, timeout=5)

    # Assert
    mock_wait.assert_called_once_with(mock_web_element, 5)
    mock_ec.assert_called_once_with(mock_web_element)
    mock_wait_instance.until.assert_called_once_with(mock_ec.return_value)

def test_wait_for_element_to_be_clickable_timeout(mock_wait, mock_web_element, mocker):
    # Arrange
    mock_wait_instance = mock_wait.return_value
    mock_wait_instance.until.side_effect = TimeoutException()
    mocker.patch("selenium.webdriver.support.expected_conditions.element_to_be_clickable")

    # Act & Assert
    with pytest.raises(TimeoutException):
        wait_for_element_to_be_clickable(mock_web_element, timeout=5)

def test_wait_for_element_to_be_in_viewport(mock_wait, mock_web_element, mocker):
    # Arrange
    mock_in_viewport = mocker.patch("webserpent.selenium.wait._in_viewport")
    mock_in_viewport.return_value = lambda _: True
    mock_wait_instance = mock_wait.return_value
    mock_wait_instance.until.return_value = None

    # Act
    wait_for_element_to_be_in_viewport(mock_web_element, timeout=5)

    # Assert
    mock_wait.assert_called_once_with(mock_web_element, 5)
    mock_wait_instance.until.assert_called_once_with(mock_in_viewport.return_value)

def test_wait_for_element_to_be_in_viewport_timeout(mock_wait, mock_web_element, mocker):
    # Arrange
    mock_in_viewport = mocker.patch("webserpent.selenium.wait._in_viewport")
    mock_in_viewport.return_value = lambda _: False
    mock_wait_instance = mock_wait.return_value
    mock_wait_instance.until.side_effect = TimeoutException()

    # Act & Assert
    with pytest.raises(TimeoutException):
        wait_for_element_to_be_in_viewport(mock_web_element, timeout=5)
