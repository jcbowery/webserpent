from webserpent.driver_management.browser_options import BrowserChoice, BrowserOptions, UnhandledAlertChoice, ChromeOptions
from webserpent.driver_management.driver_factory import get_local
from selenium.webdriver import Chrome, Firefox
import pytest

import time

@pytest.mark.parametrize('browser_choice', [
    (BrowserChoice.CHROME),
    (BrowserChoice.FIREFOX),
])
def test_options_give_browser(browser_choice):
    browser_options = BrowserOptions(browser_choice).get()
    web_driver = get_local(browser_options)

    match browser_choice:
        case BrowserChoice.CHROME:
            assert isinstance(web_driver, Chrome)
        case BrowserChoice.FIREFOX:
            assert isinstance(web_driver, Firefox)

    web_driver.quit()

@pytest.mark.parametrize('browser_choice', [
    (BrowserChoice.CHROME),
    (BrowserChoice.FIREFOX),
])
def test_headless_sets_headless(browser_choice):
    browser_options = BrowserOptions(browser_choice)
    browser_options.make_headless()
    options = browser_options.get()
    web_driver = get_local(options)

    assert '--headless' in options.arguments

    web_driver.quit()


@pytest.mark.parametrize('browser_choice, window_size, expected_size', [
    (BrowserChoice.CHROME, {'width': 1080, 'height': 920}, {'width': 1080, 'height': 920}),
    (BrowserChoice.FIREFOX, {'width': 1080, 'height': 920}, {'width': 1080, 'height': 920}),
])
def test_windowsize_sets_window_size(browser_choice, window_size, expected_size):
    browser_options_builder = BrowserOptions(browser_choice)
    browser_options_builder.set_window_size(window_size)
    options = browser_options_builder.get()
    web_driver = get_local(options)

    assert web_driver.get_window_size() == expected_size
    web_driver.quit()

@pytest.mark.parametrize('browser_choice, alert_options', [
    (BrowserChoice.CHROME, UnhandledAlertChoice.ACCEPT),
    (BrowserChoice.CHROME, UnhandledAlertChoice.ACCEPT_NOTIFY),
    (BrowserChoice.CHROME, UnhandledAlertChoice.DISMISS),
    (BrowserChoice.CHROME, UnhandledAlertChoice.DISMISS_NOTIFY),
    (BrowserChoice.CHROME, UnhandledAlertChoice.IGNORE),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.ACCEPT),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.ACCEPT_NOTIFY),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.DISMISS),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.DISMISS_NOTIFY),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.IGNORE)
])
def test_unhandled_alerts(browser_choice, alert_options):
    browser_options_builder = BrowserOptions(browser_choice)
    browser_options_builder.set_unhandled_alerts(alert_options)
    options = browser_options_builder.get()
    web_driver = get_local(options)

    assert options.unhandled_prompt_behavior == alert_options.value
    web_driver.quit()


@pytest.mark.parametrize('browser_choice', [
    (BrowserChoice.CHROME),
    (BrowserChoice.FIREFOX),
])
def test_set_ignore_ssl_errors(browser_choice):
    browser_options_builder = BrowserOptions(browser_choice)
    browser_options_builder.set_ignore_ssl_errors()
    options = browser_options_builder.get()
    web_driver = get_local(options)

    if isinstance(options, ChromeOptions):
        assert '--ignore-certificate-errors' in options.arguments
    else:
        assert options.preferences['network.proxy.allow_hijacking_localhost'] is True
        
    web_driver.quit()

@pytest.mark.parametrize('browser_choice, expected_result', [
    (BrowserChoice.CHROME, {'prefs': {'profile.default_content_setting_values.notifications': 2}}),
    (BrowserChoice.FIREFOX, False)
])
def test_disable_notifications(browser_choice, expected_result):
    browser_options_builder = BrowserOptions(browser_choice)
    browser_options_builder.set_disabling_notifications()
    options = browser_options_builder.get()
    web_driver = get_local(options)

    if browser_choice is BrowserChoice.CHROME:
        assert options.experimental_options == expected_result
    else:
        assert options.preferences['dom.webnotifications.enabled'] is expected_result
    
    web_driver.quit()

@pytest.mark.parametrize('browser_choice, expected_result', [
    (BrowserChoice.CHROME, '--disable-gpu'),
])
def test_disable_gpu(browser_choice, expected_result):
    browser_options_builder = BrowserOptions(browser_choice)
    browser_options_builder.disable_gpu_acceleration()
    options = browser_options_builder.get()
    web_driver = get_local(options)

    assert expected_result in options.arguments

    web_driver.quit()

@pytest.mark.parametrize('browser_choice, expected_result', [
    (BrowserChoice.CHROME, '--disable-extensions'),
    (BrowserChoice.FIREFOX, '--disable-extensions')
])
def test_disable_extensions(browser_choice, expected_result):
    browser_options_builder = BrowserOptions(browser_choice)
    browser_options_builder.disable_extensions()
    options = browser_options_builder.get()
    web_driver = get_local(options)

    assert expected_result in options.arguments

    web_driver.quit()