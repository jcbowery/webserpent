from webserpent.selenium.driver import Driver, NoSuchElementException, By, WebElement, NoSuchWindowException, NoSuchFrameException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_webdriver(mocker):
    yield mocker.Mock()

@pytest.fixture
def driver(mock_webdriver):
    d = Driver(mock_webdriver)
    yield d

@pytest.fixture(autouse=True)
def mock_system_logger(mocker):
    yield mocker.patch('webserpent.selenium.driver.logger')

# ********************************************Tests

def test_driver_initiation(mock_webdriver):
    d = Driver(mock_webdriver)

    assert d._driver == mock_webdriver

def test_current_url(driver, mock_system_logger):
    driver._driver.current_url = 'test_url'

    x = driver.current_url

    mock_system_logger.info.assert_called_once_with('retrieving current url')
    mock_system_logger.debug.assert_called_once_with('current url is "%s"', 'test_url')
    assert x == 'test_url'

def test_title(driver, mock_system_logger):
    driver._driver.title = 'test title'

    x = driver.title

    mock_system_logger.info.assert_called_once_with('retreiving page title')
    mock_system_logger.debug.assert_called_once_with('page title is "%s"', 'test title')
    assert x == 'test title'

def test_window_handles(driver, mock_system_logger):
    handles = ['handle1', 'handle2']
    driver._driver.window_handles = handles

    result = driver.window_handles

    mock_system_logger.info.assert_called_once_with('retrieving window handles')
    mock_system_logger.debug.assert_called_once_with('window handles are: %s', handles)
    assert result == handles

def test_current_window_handle(driver, mock_system_logger):
    handle = 'test handle'
    driver._driver.current_window_handle = handle

    result = driver.current_window_handle

    mock_system_logger.info.assert_called_once_with('retrieving current window handle')
    mock_system_logger.debug.assert_called_once_with('current window handle: %s', handle)

def test_find_element_success(mocker, driver, mock_system_logger):
    mock_webelement = mocker.Mock()
    mock_webelement.id = 'element id'
    by = By.ID
    location = 'testId'

    driver._driver.find_element.return_value = mock_webelement

    result = driver.find_element((by,location))

    mock_system_logger.info.assert_called_once_with('finding webelement with: (%s, %s)', by, location)
    mock_system_logger.debug.assert_called_once_with('found element: %s', mock_webelement.id)
    assert result == mock_webelement

def test_find_element_raises_NoSuchElementException(mocker, driver, mock_system_logger):
    driver._driver.find_element.side_effect = NoSuchElementException('no ele')
    by = By.ID
    location = 'testId'

    with pytest.raises(NoSuchElementException):
        driver.find_element((by, location))

    mock_system_logger.debug.assert_called_once_with('Element does not exist: (%s, %s)', by, location)
    mock_system_logger.error.assert_called_once_with('Error finding element: %s', mocker.ANY)

def test_find_elements_success(mocker, driver, mock_system_logger):
    mock_webelement1 = mocker.Mock()
    mock_webelement2 = mocker.Mock()
    mock_webelement3 = mocker.Mock()
    elements = [mock_webelement1, mock_webelement2, mock_webelement3]
    by = By.ID
    location = 'testId'
    driver._driver.find_elements.return_value = elements

    result = driver.find_elements((by, location))

    mock_system_logger.info.assert_called_once_with('finding webelements with: (%s, %s)', by, location)
    mock_system_logger.debug.assert_called_once_with('found elements: %s', elements)
    assert result == elements

def test_find_elements_raises_NoSuchElementException(mocker, driver, mock_system_logger):
    driver._driver.find_elements.side_effect = NoSuchElementException(' no ele')
    by = By.ID
    location = 'testId'

    with pytest.raises(NoSuchElementException):
        x = driver.find_elements((by, location))

    mock_system_logger.debug.assert_called_once_with('Elements do not exist: (%s, %s)', by, location)
    mock_system_logger.error.assert_called_once_with('Error finding elements: %s', mocker.ANY)

def test_switch_to_window_success(driver, mock_system_logger):
    handle = 'window'
    
    driver.switch_to_window(handle)

    mock_system_logger.info.assert_called_once_with('switching to window: %s', handle)
    driver._driver.switch_to.window.assert_called_once_with(handle)

def test_switch_to_window_raises_NoSuchWindowException(mocker, driver, mock_system_logger):
    handle = 'window'
    driver._driver.switch_to.window.side_effect = NoSuchWindowException('er')

    with pytest.raises(NoSuchWindowException):
        driver.switch_to_window(handle)

    mock_system_logger.debug.assert_called_once_with("window doesn't exist: %s", handle)
    mock_system_logger.error.assert_called_once_with('Error swithing to window: %s', mocker.ANY)

def test_switch_to_frame_success(mocker, driver, mock_system_logger):
    mock_webelement = mocker.Mock()
    frame = mock_webelement
    
    driver.switch_to_frame(frame)

    mock_system_logger.info.assert_called_once_with('switching to frame: %s', frame)
    driver._driver.switch_to.frame.assert_called_once_with(frame)

def test_switch_to_frame_raises_NoSuchFrameException(mocker, driver, mock_system_logger):
    mock_webelement = mocker.Mock()
    frame = mock_webelement
    driver._driver.switch_to.frame.side_effect = NoSuchFrameException()

    with pytest.raises(NoSuchFrameException):
        driver.switch_to_frame(frame)

    mock_system_logger.debug.assert_called_once_with('No frame: %s', frame)
    mock_system_logger.error('Error switching to frame: %s', mocker.ANY)

def test_take_screenshot_success(driver, mock_system_logger):
    file_path = 'test/path'

    driver.take_screenshot(file_path)

    mock_system_logger.info.assert_called_once_with('taking screenshot: %s', file_path)
    driver._driver.save_screenshot.assert_called_once_with(file_path)

def test_take_screenshot_raises_WebDriverException(mocker, driver, mock_system_logger):
    file_path = 'test/path'
    driver._driver.save_screenshot.side_effect = WebDriverException()

    with pytest.raises(WebDriverException):
        driver.take_screenshot(file_path)

    mock_system_logger.debug.assert_called_once_with('screenshot not saved to: %s', file_path)
    mock_system_logger.error.assert_called_once_with('Error saving screenshot: %s', mocker.ANY)

def test_refresh(driver, mock_system_logger):
    driver.refresh()
    mock_system_logger.infoassert_called_once_with('refrshing driver')
    driver._driver.refresh.assert_called_once()

def test_quit(driver, mock_system_logger):
    driver.quit()
    mock_system_logger.infoassert_called_once_with('quitting driver')
    driver._driver.quit.assert_called_once()