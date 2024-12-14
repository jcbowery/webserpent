import pytest
from webserpent.selenium.select import Select

@pytest.fixture
def select(mocker):
    s = Select(mocker.Mock())
    yield s

@pytest.fixture(autouse=True)
def mock_system_logger(mocker):
    yield mocker.patch('webserpent.selenium.select.logger')

def test_options(mocker, select, mock_system_logger):
    options = [mocker.Mock()]
    select._select.options = options
    
    result = select.options

    mock_system_logger.info.assert_called_once_with('Getting all options from the select element')
    mock_system_logger.debug.assert_called_once_with('Options retrieved: %s', [option.text for option in options])
    assert result == options

def test_all_selected_options(mocker, select, mock_system_logger):
    selected_options = [mocker.Mock()]
    select._select.all_selected_options = selected_options

    result = select.all_selected_options

    mock_system_logger.info.assert_called_once_with('Getting all selected options')
    mock_system_logger.debug.assert_called_once_with('Selected options: %s', [option.text for option in selected_options])
    assert result == selected_options

def test_first_selected_option(mocker, select, mock_system_logger):
    first_option = mocker.Mock()
    select._select.first_selected_option = first_option

    result = select.first_selected_option

    mock_system_logger.info.assert_called_once_with('Getting the first selected option')
    mock_system_logger.debug.assert_called_once_with('First selected option: %s', first_option.text)
    assert result == first_option

def test_select_by_value(mocker, select, mock_system_logger):
    value = "value1"
    select._select.select_by_value = mocker.Mock()

    select.select_by_value(value)

    select._select.select_by_value.assert_called_once_with(value)
    mock_system_logger.info.assert_called_once_with('Selecting option by value: %s', value)
    mock_system_logger.debug.assert_called_once_with("Option with value '%s' selected", value)

def test_select_by_visible_text(mocker, select, mock_system_logger):
    text = "Option Text"
    select._select.select_by_visible_text = mocker.Mock()

    select.select_by_visible_text(text)

    select._select.select_by_visible_text.assert_called_once_with(text)
    mock_system_logger.info.assert_called_once_with('Selecting option by visible text: %s', text)
    mock_system_logger.debug.assert_called_once_with("Option with visible text '%s' selected", text)

def test_select_by_index(mocker, select, mock_system_logger):
    index = 1
    select._select.select_by_index = mocker.Mock()

    select.select_by_index(index)

    select._select.select_by_index.assert_called_once_with(index)
    mock_system_logger.info.assert_called_once_with('Selecting option by index: %d', index)
    mock_system_logger.debug.assert_called_once_with("Option at index '%d' selected", index)

def test_deselect_all(mocker, select, mock_system_logger):
    select._select.deselect_all = mocker.Mock()

    select.deselect_all()

    select._select.deselect_all.assert_called_once()
    mock_system_logger.info.assert_called_once_with('Deselecting all options')
    mock_system_logger.debug.assert_called_once_with("All options deselected")

def test_deselect_by_value(mocker, select, mock_system_logger):
    value = "value1"
    select._select.deselect_by_value = mocker.Mock()

    select.deselect_by_value(value)

    select._select.deselect_by_value.assert_called_once_with(value)
    mock_system_logger.info.assert_called_once_with('Deselecting option by value: %s', value)
    mock_system_logger.debug.assert_called_once_with("Option with value '%s' deselected", value)

def test_deselect_by_visible_text(mocker, select, mock_system_logger):
    text = "Option Text"
    select._select.deselect_by_visible_text = mocker.Mock()

    select.deselect_by_visible_text(text)

    select._select.deselect_by_visible_text.assert_called_once_with(text)
    mock_system_logger.info.assert_called_once_with('Deselecting option by visible text: %s', text)
    mock_system_logger.debug.assert_called_once_with("Option with visible text '%s' deselected", text)

def test_deselect_by_index(mocker, select, mock_system_logger):
    index = 1
    select._select.deselect_by_index = mocker.Mock()

    select.deselect_by_index(index)

    select._select.deselect_by_index.assert_called_once_with(index)
    mock_system_logger.info.assert_called_once_with('Deselecting option by index: %d', index)
    mock_system_logger.debug.assert_called_once_with("Option at index '%d' deselected", index)
