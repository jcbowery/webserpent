import pytest
from unittest.mock import MagicMock
from selenium.webdriver.common.alert import Alert as SeleniumAlert
from webserpent.selenium.alert import Alert

@pytest.fixture
def mock_selenium_alert():
    return MagicMock(spec=SeleniumAlert)

@pytest.fixture
def alert(mock_selenium_alert):
    return Alert(mock_selenium_alert)

def test_text_property(alert, mock_selenium_alert, mocker):
    mock_selenium_alert.text = "Test Alert Text"
    mock_logger = mocker.patch("webserpent.selenium.alert.logger")

    text = alert.text

    assert text == "Test Alert Text"
    mock_logger.info.assert_called_once_with('Getting alert text')
    mock_logger.debug.assert_called_once_with('Alert text: %s', "Test Alert Text")

def test_dismiss(alert, mock_selenium_alert, mocker):
    mock_logger = mocker.patch("webserpent.selenium.alert.logger")

    alert.dismiss()

    mock_selenium_alert.dismiss.assert_called_once()
    mock_logger.info.assert_called_once_with('Dismissing the alert')
    mock_logger.debug.assert_called_once_with('Alert dismissed successfully')

def test_dismiss_exception(alert, mock_selenium_alert, mocker):
    mock_logger = mocker.patch("webserpent.selenium.alert.logger")
    mock_selenium_alert.dismiss.side_effect = Exception("Dismiss Error")

    with pytest.raises(Exception, match="Dismiss Error"):
        alert.dismiss()

    mock_logger.info.assert_called_once_with('Dismissing the alert')
    mock_logger.error.assert_called_once_with('Failed to dismiss alert: %s', mock_selenium_alert.dismiss.side_effect)

def test_accept(alert, mock_selenium_alert, mocker):
    mock_logger = mocker.patch("webserpent.selenium.alert.logger")

    alert.accept()

    mock_selenium_alert.accept.assert_called_once()
    mock_logger.info.assert_called_once_with('Accepting the alert')
    mock_logger.debug.assert_called_once_with('Alert accepted successfully')

def test_accept_exception(alert, mock_selenium_alert, mocker):
    mock_logger = mocker.patch("webserpent.selenium.alert.logger")
    mock_selenium_alert.accept.side_effect = Exception("Accept Error")

    with pytest.raises(Exception, match="Accept Error"):
        alert.accept()

    mock_logger.info.assert_called_once_with('Accepting the alert')
    mock_logger.error.assert_called_once_with('Failed to accept alert: %s', mock_selenium_alert.accept.side_effect)

def test_send_keys(alert, mock_selenium_alert, mocker):
    keys_to_send = "Test Keys"
    mock_logger = mocker.patch("webserpent.selenium.alert.logger")

    alert.send_keys(keys_to_send)

    mock_selenium_alert.send_keys.assert_called_once_with(keys_to_send)
    mock_logger.info.assert_called_once_with('Sending keys to alert: %s', keys_to_send)
    mock_logger.debug.assert_called_once_with('Keys sent to alert successfully')

def test_send_keys_exception(alert, mock_selenium_alert, mocker):
    keys_to_send = "Test Keys"
    mock_logger = mocker.patch("webserpent.selenium.alert.logger")
    mock_selenium_alert.send_keys.side_effect = Exception("Send Keys Error")

    with pytest.raises(Exception, match="Send Keys Error"):
        alert.send_keys(keys_to_send)

    mock_logger.info.assert_called_once_with('Sending keys to alert: %s', keys_to_send)
    mock_logger.error.assert_called_once_with('Failed to send keys to alert: %s', mock_selenium_alert.send_keys.side_effect)
