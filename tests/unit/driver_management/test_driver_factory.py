import pytest
from unittest.mock import MagicMock, patch

from webserpent.driver_management.driver_factory import get_local
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions


@pytest.fixture(params=[ChromeOptions(), FirefoxOptions(), SafariOptions()])
def browser_options(request):
    # Fixture to provide different browser options
    return request.param


def test_get_local_returns_proper_driver(browser_options):
    with patch('selenium.webdriver.Chrome') as mock_chrome_driver, \
         patch('selenium.webdriver.Firefox') as mock_firefox_driver, \
         patch('selenium.webdriver.Safari') as mock_safari_driver:
        
        # Mocked drivers
        mock_chrome_driver.return_value = MagicMock(name="MockChromeDriver")
        mock_firefox_driver.return_value = MagicMock(name="MockFirefoxDriver")
        mock_safari_driver.return_value = MagicMock(name="MockSafariDriver")
        
        # Invoke the DriverFactory
        result = get_local(browser_options)

        # Assert based on the browser option provided
        if isinstance(browser_options, ChromeOptions):
            mock_chrome_driver.assert_called_once_with(options=browser_options)
            assert result == mock_chrome_driver.return_value
        elif isinstance(browser_options, FirefoxOptions):
            mock_firefox_driver.assert_called_once_with(options=browser_options)
            assert result == mock_firefox_driver.return_value
        elif isinstance(browser_options, SafariOptions):
            mock_safari_driver.assert_called_once_with(options=browser_options)
            assert result == mock_safari_driver.return_value
        else:
            pytest.fail("Unsupported browser option provided")
