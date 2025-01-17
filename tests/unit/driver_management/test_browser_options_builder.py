import pytest
from webserpent.driver_management.browser_options import BrowserOptions, BrowserChoice, UnhandledAlertChoice
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions


@pytest.fixture
def browser_options(mocker, request):
    # Get the browser choice from the test parameter
    browser_choice = request.param

    # Spy on the options classes
    if browser_choice == BrowserChoice.CHROME:
        spy_options = ChromeOptions()
        mocker.spy(spy_options, "add_argument")
        mocker.spy(spy_options, "add_experimental_option")
    elif browser_choice == BrowserChoice.FIREFOX:
        spy_options = FirefoxOptions()
        mocker.spy(spy_options, "add_argument")
        mocker.spy(spy_options, "set_preference")
    elif browser_choice == BrowserChoice.SAFARI:
        spy_options = SafariOptions()
        mocker.spy(spy_options, "add_argument")
    else:
        raise ValueError(f"Unsupported browser choice: {browser_choice}")

    # Mock the `_set_options` method to prevent real initialization
    mocker.patch('webserpent.driver_management.browser_options.BrowserOptions._set_options')

    # Create the BrowserOptions instance
    bo = BrowserOptions(browser_choice)
    bo._options = spy_options
    yield bo


@pytest.mark.parametrize("browser_choice, expected_options_class", [
    (BrowserChoice.CHROME, ChromeOptions),
    (BrowserChoice.FIREFOX, FirefoxOptions),
    (BrowserChoice.SAFARI, SafariOptions)
])
def test_browser_options_init(browser_choice, expected_options_class):
    browser_options = BrowserOptions(browser_choice)

    assert isinstance(browser_options._options, expected_options_class)


@pytest.mark.parametrize("browser_options, should_call", [
    (BrowserChoice.CHROME, True),
    (BrowserChoice.FIREFOX, True),
    (BrowserChoice.SAFARI, False),
], indirect=["browser_options"])
def test_headless_adds_headless_argument(browser_options, should_call):
    browser_options.make_headless()

    if should_call:
        browser_options._options.add_argument.assert_called_once_with('--headless')
    else:
        browser_options._options.add_argument.assert_not_called()


@pytest.mark.parametrize("browser_options, input, argument", [
    (BrowserChoice.CHROME, {"width": 1920, "height": 1080}, '--window-size=1920,1080'),
    (BrowserChoice.FIREFOX, {"width": 1920, "height": 1080}, ['--width=1920', '--height=1080']),
    (BrowserChoice.SAFARI, {"width": 1920, "height": 1080}, '--window-size=1920,1080'),
], indirect=["browser_options"])
def test_set_window_size_adds_correct_argument(mocker, browser_options, input, argument):
    browser_options.set_window_size(input)

    if isinstance(browser_options._options, FirefoxOptions):
        browser_options._options.add_argument.assert_has_calls([
            mocker.call('--width=1920'),
            mocker.call('--height=1080')
        ])
    else:
        browser_options._options.add_argument.assert_called_once_with(argument)



@pytest.mark.parametrize("browser_options, input, msg", [
    (BrowserChoice.CHROME, '{"width": 1920, "height": 1080}', "Expected a dict with keys 'width' and 'height'"),
    (BrowserChoice.FIREFOX, '{"width": 1920, "height": 1080}', "Expected a dict with keys 'width' and 'height'"),
    (BrowserChoice.SAFARI, '{"width": 1920, "height": 1080}', "Expected a dict with keys 'width' and 'height'"),
    (BrowserChoice.CHROME, {"apple": 1920, "orange": 1080}, "Expected a dict with exactly two keys: 'width' and 'height'"),
    (BrowserChoice.FIREFOX, {"apple": 1920, "orange": 1080}, "Expected a dict with exactly two keys: 'width' and 'height'"),
    (BrowserChoice.SAFARI, {"apple": 1920, "orange": 1080}, "Expected a dict with exactly two keys: 'width' and 'height'"),
], indirect=["browser_options"])
def test_set_window_size_throws_ValueError(browser_options, input, msg):
    with pytest.raises(TypeError, match=msg):
        browser_options.set_window_size(input)


@pytest.mark.parametrize("browser_options, input, value", [
    (BrowserChoice.CHROME, UnhandledAlertChoice.ACCEPT, UnhandledAlertChoice.ACCEPT.value),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.ACCEPT, UnhandledAlertChoice.ACCEPT.value),
    (BrowserChoice.SAFARI, UnhandledAlertChoice.ACCEPT, UnhandledAlertChoice.ACCEPT.value),
    (BrowserChoice.CHROME, UnhandledAlertChoice.DISMISS, UnhandledAlertChoice.DISMISS.value),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.DISMISS, UnhandledAlertChoice.DISMISS.value),
    (BrowserChoice.SAFARI, UnhandledAlertChoice.DISMISS, UnhandledAlertChoice.DISMISS.value),
    (BrowserChoice.CHROME, UnhandledAlertChoice.DISMISS_NOTIFY, UnhandledAlertChoice.DISMISS_NOTIFY.value),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.DISMISS_NOTIFY, UnhandledAlertChoice.DISMISS_NOTIFY.value),
    (BrowserChoice.SAFARI, UnhandledAlertChoice.DISMISS_NOTIFY, UnhandledAlertChoice.DISMISS_NOTIFY.value),
    (BrowserChoice.CHROME, UnhandledAlertChoice.ACCEPT_NOTIFY, UnhandledAlertChoice.ACCEPT_NOTIFY.value),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.ACCEPT_NOTIFY, UnhandledAlertChoice.ACCEPT_NOTIFY.value),
    (BrowserChoice.SAFARI, UnhandledAlertChoice.ACCEPT_NOTIFY, UnhandledAlertChoice.ACCEPT_NOTIFY.value),
    (BrowserChoice.CHROME, UnhandledAlertChoice.IGNORE, UnhandledAlertChoice.IGNORE.value),
    (BrowserChoice.FIREFOX, UnhandledAlertChoice.IGNORE, UnhandledAlertChoice.IGNORE.value),
    (BrowserChoice.SAFARI, UnhandledAlertChoice.IGNORE, UnhandledAlertChoice.IGNORE.value),
], indirect=["browser_options"])
def test_set_unhandled_alerts_sets_expected_value(browser_options, input, value):
    browser_options.set_unhandled_alerts(input)
    
    actual = browser_options._options.unhandled_prompt_behavior
    assert actual == value, f'wanted {value} but got: {actual}'


@pytest.mark.parametrize("browser_options, value", [
    (BrowserChoice.CHROME, "--ignore-certificate-errors"),
    (BrowserChoice.FIREFOX, ("network.proxy.allow_hijacking_localhost", True)),
    (BrowserChoice.SAFARI, None),
], indirect=["browser_options"])
def test_set_ignore_ssl_errors(browser_options, value):
    browser_options.set_ignore_ssl_errors()
    
    if isinstance(browser_options._options, ChromeOptions):
        browser_options._options.add_argument.assert_called_once_with(value)
    elif isinstance(browser_options._options, FirefoxOptions):
        browser_options._options.set_preference.assert_called_once_with(*value)
        
    else:
        browser_options._options.add_argument.assert_not_called()


@pytest.mark.parametrize("browser_options, value", [
    (BrowserChoice.CHROME, ("prefs", {"profile.default_content_setting_values.notifications": 2})),
    (BrowserChoice.FIREFOX, ("dom.webnotifications.enabled", False)),
    (BrowserChoice.SAFARI, None),
], indirect=["browser_options"])
def test_set_disabling_notifications(browser_options, value):
    browser_options.set_disabling_notifications()
    
    if isinstance(browser_options._options, ChromeOptions):
        browser_options._options.add_experimental_option.assert_called_once_with(*value)
    elif isinstance(browser_options._options, FirefoxOptions):
        browser_options._options.set_preference.assert_called_once_with(*value)
        
    else:
        browser_options._options.add_argument.assert_not_called()


@pytest.mark.parametrize("browser_options, should_call", [
    (BrowserChoice.CHROME, True),
    (BrowserChoice.FIREFOX, False),
    (BrowserChoice.SAFARI, False),
], indirect=["browser_options"])
def test_disable_gpu_acceleration(browser_options, should_call):
    browser_options.disable_gpu_acceleration()

    if should_call:
        # Assert the method was called with the correct argument
        browser_options._options.add_argument.assert_called_once_with('--disable-gpu')
    else:
        # Assert the method was not called
        browser_options._options.add_argument.assert_not_called()

@pytest.mark.parametrize("browser_options", [
    (BrowserChoice.CHROME),
    (BrowserChoice.FIREFOX),
    (BrowserChoice.SAFARI),
], indirect=["browser_options"])
def test_disable_gextensions(browser_options):
    browser_options.disable_extensions()

    browser_options._options.add_argument.assert_called_once_with('--disable-extensions')

@pytest.mark.parametrize("browser_options, device_name", [
    (BrowserChoice.CHROME, 'iPhone X'),
    (BrowserChoice.FIREFOX, False),
    (BrowserChoice.SAFARI, False),
], indirect=["browser_options"])
def test_set_emulate_mobile_device(browser_options, device_name):
    browser_options.set_emulate_mobile_device(device_name)

    if device_name:
        browser_options._options.add_experimental_option.assert_called_once_with("mobileEmulation", {"deviceName": device_name})


@pytest.mark.parametrize("browser_options, log_lvl", [
    (BrowserChoice.CHROME, 3),
    (BrowserChoice.FIREFOX, False),
    (BrowserChoice.SAFARI, False),
], indirect=["browser_options"])
def test_set_logging_preference(browser_options, log_lvl):
    browser_options.set_logging_preference(log_lvl)

    if log_lvl:
        browser_options._options.add_argument.assert_called_once_with(f"--log-level={log_lvl}")
    else:
        browser_options._options.add_argument.assert_not_called()


@pytest.mark.parametrize("browser_options, should_run", [
    (BrowserChoice.CHROME, True),
    (BrowserChoice.FIREFOX, False),
    (BrowserChoice.SAFARI, False),
], indirect=["browser_options"])
def test_dsiable_infobars(browser_options, should_run):
    browser_options.disable_infobars()

    if should_run:
        browser_options._options.add_argument.assert_called_once_with("--disable-infobars")
    else:
        browser_options._options.add_argument.assert_not_called()

@pytest.mark.parametrize("browser_options, option", [
    (BrowserChoice.CHROME, True),
    (BrowserChoice.FIREFOX, False),
    (BrowserChoice.SAFARI, False),
], indirect=["browser_options"])
def test_enable_experimental_webdriver_features(browser_options, option):
    browser_options.enable_experimental_webdriver_features()
    if option:
        browser_options._options.add_experimental_option.assert_called_once_with("excludeSwitches", ["enable-automation"])

@pytest.mark.parametrize("browser_options, option_type", [
    (BrowserChoice.CHROME, ChromeOptions),
    (BrowserChoice.FIREFOX, FirefoxOptions),
    (BrowserChoice.SAFARI, SafariOptions),
], indirect=["browser_options"])
def test_get(browser_options, option_type):
    result = browser_options.get()

    assert isinstance(result, option_type)