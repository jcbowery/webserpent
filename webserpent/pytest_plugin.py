"""pytest plugin"""

from datetime import datetime

import pytest

from webserpent.driver_management.driver_factory import DriverFactory
from webserpent.driver_management.options_builder import OptionsBuilder
from webserpent.enums import BrowserType
from webserpent.logging.logger import get_system_logger, setup_test_logger
from webserpent.configurations.configs import CONFIGS

logger = get_system_logger(__name__)


def pytest_addoption(parser):
    """
    Add custom command-line options for browser selection
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="specify the browser to run tests in: chrome, firefox, safari",
    )
    parser.addoption(
        "--browser_version",
        action="store",
        default=None,
        help="specify the browser version to use",
    )
    parser.addoption(
        "--gui",
        action="store_true",
        default=False,
        help="specify the browser version to use",
    )

@pytest.fixture(scope="session")
def browser(request):
    """
    Fixture to provide browser from command-line option
    """
    browser_input = request.config.getoption("--browser")
    match browser_input.lower():
        case "chrome":
            browser_choice = BrowserType.CHROME
        case "firefox":
            browser_choice = BrowserType.FIREFOX
        case "safari":
            browser_choice = BrowserType.SAFARI
        case _:
            logger.critical(
                "can only enter chrome, firefox, or safari, got: %s", browser_input
            )
            raise ValueError(f"Incorrect browser input option: {browser_input}")
    yield browser_choice

@pytest.fixture(scope="session")
def browser_version(request):
    """
    Fixture to provide browser version from command-line option
    """
    return request.config.getoption("--browser_version")

@pytest.fixture(scope="function")
def function_name(request):
    """get the function name for test"""
    # Get the name of the test function
    test_name = request.node.name
    # Remove the "test_" prefix
    clean_name = test_name[5:] if test_name.startswith("test_") else test_name
    return clean_name

@pytest.fixture(scope="function")
def test_logger(function_name):
    """generate the test logger"""
    date_str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    test_logger_object = setup_test_logger(
        CONFIGS.SYSTEM.log_level,
        function_name,
        "Logs",
        f"{function_name+date_str}.txt",
    )
    yield test_logger_object

@pytest.fixture(scope="function")
def browser_options(request, browser, browser_version, test_logger):
    """get browser options"""
    logger.info("Setting browser options")
    options_builder = OptionsBuilder(browser, test_logger)
    # set browser version
    if browser_version:
        options_builder.set_browser_version(browser_version)
    # set headless
    if not request.config.getoption("--gui") and CONFIGS.WEBDRIVER.headless:
        options_builder.headless()
    # set implicit wait timeout
    if CONFIGS.TIMEOUTS.implicit > 0:
        options_builder.set_implicit_wait_timout(CONFIGS.TIMEOUTS.implicit)
    # set pageload timeout
    options_builder.set_page_load_timeout(CONFIGS.TIMEOUTS.page_load)

    yield options_builder.get()

@pytest.fixture(scope="function")
def driver(test_logger, browser, browser_options):
    """get driver"""
    web_driver = DriverFactory.get_local(test_logger, browser, browser_options)
    yield web_driver
    web_driver.quit()
