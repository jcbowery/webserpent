# from unittest.mock import Mock

# import pytest

# from webserpent.selenium.element import (
#     By,
#     CONFIGS,
#     Element,
#     ElementClickInterceptedException,
#     ElementNotInteractableException,
# )
# import logging


# @pytest.fixture(scope="function")
# def webelement_mock(mocker):
#     yield mocker.Mock()


# @pytest.fixture
# def element_name():
#     yield "element_name"


# @pytest.fixture
# def system_logger_mock(mocker):
#     yield mocker.Mock()

# @pytest.fixture
# def test_logger_mock(mocker):
#     yield mocker.Mock()

# @pytest.fixture
# def element(webelement_mock, system_logger_mock, test_logger_mock):
#     element = Element(webelement_mock, 'test element', test_logger_mock)
#     yield element


# @pytest.fixture(autouse=True, scope="function")
# def patch_system_logger(mocker, system_logger_mock):
#     mocker.patch("webserpent.selenium.element.logger", system_logger_mock)

# @pytest.fixture
# def log_message_mock(mocker):
#     return mocker.patch('webserpent.selenium.element.log_message')


# @pytest.fixture(autouse=True)
# def mock_wait(mocker):
#     wait_mock = mocker.patch('webserpent.selenium.element.Wait')
#     wait_instance = mocker.Mock()
#     wait_mock.return_value = wait_instance
#     return wait_mock, wait_instance


# # ********************************************* Tests


# def test_element_class(webelement_mock, test_logger_mock):
#     name = "element_name"
#     element = Element(webelement_mock, name, test_logger_mock)

#     assert isinstance(element, Element)
#     assert element._element == webelement_mock
#     assert element._name == name
#     assert element._logger == test_logger_mock

# def test_click_success(mocker, element, system_logger_mock, log_message_mock, mock_wait):
#     # Arrange: Set up mocks and expectations
#     element_interactable = mocker.patch('webserpent.selenium.element.EC.element_to_be_clickable')
#     wait_mock, wait_instance = mock_wait

#     # Act: Call the method under test
#     element.click()

#     # Assert: Verify behavior and interactions
#     log_message_mock.assert_called_once_with(
#         [system_logger_mock, element._logger],
#         logging.INFO,
#         'clicking on (test element)'
#     )
#     wait_mock.assert_called_once_with(CONFIGS.TIMEOUTS.element_interaction)
#     wait_instance.until.assert_called_once_with(element_interactable())
#     element._element.click.assert_called_once()

# def test_click_raises_ElementClickInterceptedException(element, system_logger_mock, log_message_mock):
#     element._element.click.side_effect = ElementClickInterceptedException()
    
#     element.click()

#     log_message_mock.assert_called_with(
#         [system_logger_mock, element._logger],
#         logging.WARNING,
#         'click on (test element) intercepted. Attempting a js click'
#     )
#     element._element.parent.execute_script.assert_called_once_with("arguments[0].click();", element._element)

# def test_click_raises_ElementNotInteractableException(mocker, element, system_logger_mock, log_message_mock):
#     element._element.click.side_effect = [ElementNotInteractableException(), None]
#     scroll_method_mock = mocker.patch('webserpent.selenium.element.Element.scroll_to')

#     element.click()

#     log_message_mock.assert_called_with(
#         [system_logger_mock, element._logger],
#         logging.WARNING,
#         '(test element) not interactable. Scrolling to element to try again.'
#     )
#     scroll_method_mock.assert_called_once()
#     assert element._element.click.call_count == 2

# def test_click_raises_unexpectedError(mocker, element, system_logger_mock, log_message_mock):
#     element._element.click.side_effect = Exception('error msg')

#     with pytest.raises(Exception):
#         element.click()

#     log_message_mock.assert_called_with(
#         [system_logger_mock, element._logger],
#         logging.ERROR,
#         'unknown error clicking (test element): error msg'
#     )


# def test_scroll_to(mocker, element, mock_wait):
#     mock_in_viewport = mocker.patch('webserpent.selenium.element.Element.in_viewport')
#     mock_is_true = mocker.patch('webserpent.selenium.element.is_true')
    
#     element.scroll_to()

#     element._element.parent.execute_script.assert_called_once_with("arguments[0].scrollIntoView(true);", element._element)
#     mock_wait[1].until.assert_called_once_with(mock_is_true())

# def test_in_viewport(mocker, webelement_mock, element):
#     # Mock JavaScript execution to return a specific result
#     js_return_value = {
#         "top": True,
#         "bottom": True,
#         "left": True,
#         "right": True
#     }
#     execute_script_mock = mocker.patch.object(
#         webelement_mock.parent, 
#         'execute_script',
#         return_value=js_return_value
#     )
    
#     element 

#     # Assert that in_viewport returns True when the mocked JS values are within the viewport
#     assert element.in_viewport is True

#     # Verify that the JS was called with the correct script and arguments
#     execute_script_mock.assert_called_once_with(
#         """
#             var rect = arguments[0].getBoundingClientRect();
#             var viewWidth = window.innerWidth || document.documentElement.clientWidth;
#             var viewHeight = window.innerHeight || document.documentElement.clientHeight;
#             return {
#                 top: rect.top >= 0 && rect.top < viewHeight,
#                 bottom: rect.bottom <= viewHeight,
#                 left: rect.left >= 0 && rect.left < viewWidth,
#                 right: rect.right <= viewWidth
#             };
#         """,
#         webelement_mock,
#     )

# def test_force_click(mocker, system_logger_mock, element, log_message_mock):
#     scroll_to_method = mocker.patch('webserpent.selenium.element.Element.scroll_to')
    
#     element.force_click()

#     element._element.parent.execute_script.assert_called_once_with(
#         "arguments[0].click();", element._element
#     )
#     scroll_to_method.assert_called_once()
#     log_message_mock.assert_called_once_with(
#         [system_logger_mock, element._logger],
#         logging.INFO,
#         'scrolling to and clicking on (test element) with js'
#     )

# def test_send_keys(system_logger_mock, element, log_message_mock):
#     text = 'my_text'
    
#     element.send_keys(text)

#     element._element.send_keys.assert_called_once_with(text)
#     log_message_mock.assert_called_once_with(
#         [system_logger_mock, element._logger],
#         logging.INFO,
#         f'sending "{text}" to (test element)'
#     )

# def test_send_keys_on_error(mocker, system_logger_mock, log_message_mock, element):
#     text = 'my_text'
#     element._element.send_keys.side_effect = Exception('my msg')

#     with pytest.raises(Exception):
#         element.send_keys(text)

#     log_message_mock.assert_called_with(
#         [system_logger_mock, element._logger],
#         logging.ERROR,
#         f'error sending "{text}" to (test element): my msg'
#     )

# def test_find_element(mocker, webelement_mock, element_name, system_logger_mock, element, log_message_mock, mock_wait):
#     mock_presence_of_element = mocker.patch(
#         "webserpent.selenium.element.EC.presence_of_element_located",
#         autospec=True,
#     )
#     locator_id = 'my_id'
#     new_name = 'my_new_name'
#     new_webelement_mock = mocker.Mock()
#     element._element.find_element.return_value = new_webelement_mock
     
#     outcome = element.find_element((By.ID, locator_id), new_name)

#     log_message_mock.assert_called_with(
#         [system_logger_mock, element._logger],
#         logging.INFO,
#         f'searching for element with: {(By.ID, locator_id)} from ({element._name})'
#     )
#     mock_wait[1].until.assert_called_once_with(
#         mock_presence_of_element((By.ID, locator_id))
#     )

#     webelement_mock.find_element.assert_called_once_with((By.ID, locator_id))
#     assert isinstance(outcome, Element)
#     assert outcome._name == new_name
#     assert outcome._element == new_webelement_mock

# def test_text_property_returns_element_text(mocker, webelement_mock, system_logger_mock):
#     # mocksetup
#     webelement_mock.text = 'my element text'
#     test_logger_mock = mocker.Mock()
#     log_method_mock = mocker.patch('webserpent.selenium.element.log_message')
#     # Object setup
#     element = Element(webelement_mock, name='test element', test_logger=test_logger_mock)

#     # perform
#     text = element.text

#     # test
#     assert text == 'my element text'
#     log_method_mock.assert_called_once_with([system_logger_mock, test_logger_mock], logging.INFO, 'Returning text from (test element)')

# def test_is_displayed_returns_true(mocker, webelement_mock, system_logger_mock):
#     # mocksetup
#     webelement_mock.isdisplayed = True
#     test_logger_mock = mocker.Mock()
#     log_method_mock = mocker.patch('webserpent.selenium.element.log_message')
#     # Object setup
#     element = Element(webelement_mock, name='test element', test_logger=test_logger_mock)

#     # perform
#     is_displayed = element.is_displayed

#     # test
#     assert is_displayed
#     log_method_mock.assert_called_once_with([system_logger_mock, test_logger_mock], logging.INFO, 'Returning whether (test element) is displayed')

# def test_is_enabled_returns_true(mocker, webelement_mock, system_logger_mock):
#     # mocksetup
#     webelement_mock.is_enabled = True
#     test_logger_mock = mocker.Mock()
#     log_method_mock = mocker.patch('webserpent.selenium.element.log_message')
#     # Object setup
#     element = Element(webelement_mock, name='test element', test_logger=test_logger_mock)

#     # perform
#     is_enabled = element.is_enabled

#     # test
#     assert is_enabled
#     log_method_mock.assert_called_once_with([system_logger_mock, test_logger_mock], logging.INFO, 'Returning whether (test element) is enabled')

# def test_is_selected_returns_true(mocker, webelement_mock, system_logger_mock):
#     # mocksetup
#     webelement_mock.is_selected = True
#     test_logger_mock = mocker.Mock()
#     log_method_mock = mocker.patch('webserpent.selenium.element.log_message')
#     # Object setup
#     element = Element(webelement_mock, name='test element', test_logger=test_logger_mock)

#     # perform
#     is_selected = element.is_selected

#     # test
#     assert is_selected
#     log_method_mock.assert_called_once_with([system_logger_mock, test_logger_mock], logging.INFO, 'Returning whether (test element) is selected')

# def test_clear(element, system_logger_mock, log_message_mock):
#     element.clear()

#     element._element.clear.assert_called_once()
#     log_message_mock.assert_called_once_with(
#         [system_logger_mock, element._logger],
#         logging.INFO,
#         f"clearing (test element)"
#     )

# def test_get_attribute(element, system_logger_mock, log_message_mock):
#     element._element.get_attribute.return_value = 'my att'

#     actual = element.get_attribute('x')

#     log_message_mock.assert_called_once_with(
#         [system_logger_mock, element._logger],
#         logging.INFO,
#         'returning "x" attribute from (test element)'
#     )
#     element._element.get_attribute.assert_called_once()
#     assert actual == 'my att'

# def test_get_css_value(element, system_logger_mock, log_message_mock):
#     element._element.value_of_css_property.return_value = 'my prop'

#     actual = element.get_css_value('x')

#     log_message_mock.assert_called_once_with(
#         [system_logger_mock, element._logger],
#         logging.INFO,
#         f'returning "x" css property value from (test element)'
#     )
#     element._element.value_of_css_property.assert_called_once()
#     assert actual == 'my prop'