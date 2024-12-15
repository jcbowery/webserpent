"""pytest plugin"""

from datetime import datetime

from webserpent.configurations.configs import CONFIGS
from webserpent.driver_management.options_builder import OptionsBuilder
from webserpent.enums import BrowserType
from webserpent.enums import string_to_enum
from webserpent.logging.logger import get_system_logger, setup_test_logger

logger = get_system_logger(__name__)


def pytest_addoption(parser):
    """
    Add custom command-line options for browser selection
    """
    parser.addoption(
        "--browser",
        action="store",
        default=None,
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


def _get_logger(request):
    return setup_test_logger(
        CONFIGS.system.log_level,
        request.node.name,
        CONFIGS.system.log_dir_path,
        _generate_log_name(request.node.name),
    )


def _build_options(request):
    browser_choice = request.config.getoption("--browser")
    if browser_choice:
        CONFIGS.webdriver.browser_type = string_to_enum(browser_choice, BrowserType)
    options_builder = OptionsBuilder(CONFIGS.webdriver.browser_type)

    # Browser Version
    browser_version = request.config.getoption("--browser_version")
    if browser_version:
        CONFIGS.webdriver.browser_version = browser_version
    if CONFIGS.webdriver.browser_version:
        options_builder.set_browser_version(CONFIGS.webdriver.browser_version)

    # Page load timeout
    options_builder.set_page_load_timeout(CONFIGS.timeouts.page_load)

    # Implicit Wait Time
    if CONFIGS.timeouts.implicit:
        options_builder.set_implicit_wait_timeout(CONFIGS.timeouts.implicit)

    # Headless
    if request.config.getoption("--gui"):
        CONFIGS.webdriver.headless = True
    if CONFIGS.webdriver.headless:
        options_builder.headless()

    # Window Size
    options_builder.set_window_size(
        CONFIGS.webdriver.window_size.get("width"),
        CONFIGS.webdriver.window_size.get("height"),
    )

    # Binary location
    if CONFIGS.system.binary_dir_path:
        options_builder.set_binary_location(CONFIGS.system.binary_dir_path)

    # TODO: finish browser options

    return options_builder.get()


def _generate_log_name(test_name):
    # Get the current time and format it as "YYYYMMDDHHMMSS"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # Combine the test name with the timestamp
    return f"{test_name}_{timestamp}.txt"
