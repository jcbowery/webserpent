import pytest
from unittest.mock import MagicMock
from webserpent.configs import set_configs, WebDriverConfigs, Timeouts, _serialize_toml, WebSerpentConfigs
import time

@pytest.fixture
def mock_path_exists(mocker):
    """Mock Path.exists method"""
    return mocker.patch("webserpent.configs.Path.exists")

@pytest.fixture
def mock_toml_load(mocker):
    """Mock toml.load method"""
    return mocker.patch("webserpent.configs.toml.load")

def test_set_configs_no_toml(mock_path_exists):
    """Test default configuration when no webserpent.toml exists"""
    mock_path_exists.return_value = False  # Simulate missing toml file
    webdriver_configs, webserpent_configs = set_configs()
    assert isinstance(webdriver_configs, WebDriverConfigs)
    assert isinstance(webserpent_configs, WebSerpentConfigs)
    assert webdriver_configs.headless is True
    assert isinstance(webdriver_configs.timeouts, Timeouts)
    assert webdriver_configs.timeouts.page_load == 10
    assert webdriver_configs.timeouts.find_element == 5

def test_set_configs_with_toml(mock_path_exists, mock_toml_load):
    """Test configuration loading from webserpent.toml"""
    mock_path_exists.return_value = True  # Simulate toml file presence
    mock_toml_load.return_value = {
        "webdriver": {
            "headless": False,
            "timeouts": {
                "implicit": 15,
                "page_load": 20,
                "find_element": 10,
                "element_interaction": 5,
            },
        }
    }
    webdriver_configs, _ = set_configs()
    assert isinstance(webdriver_configs, WebDriverConfigs)
    assert webdriver_configs.headless is False
    assert webdriver_configs.timeouts.implicit == 15
    assert webdriver_configs.timeouts.page_load == 20
    assert webdriver_configs.timeouts.find_element == 10
    assert webdriver_configs.timeouts.element_interaction == 5

def test_serialize_toml_success(mock_toml_load):
    """Test successful serialization of toml file"""
    mock_toml_load.return_value = {
        "webdriver": {"headless": True, "timeouts": {"implicit": 10}}
    }
    result = _serialize_toml("webserpent.toml")
    assert result["webdriver"]["headless"] is True
    assert result["webdriver"]["timeouts"]["implicit"] == 10

def test_serialize_toml_failure(mocker, mock_toml_load):
    """Test failure in serializing toml file"""
    mock_toml_load.side_effect = Exception("Error loading toml")
    with pytest.raises(Exception, match="Error loading toml"):
        _serialize_toml("webserpent.toml")

def test_invalid_timeouts_type():
    """Test invalid timeouts type raises TypeError"""
    with pytest.raises(TypeError, match="expected 'page_load' to be an int"):
        timeouts = Timeouts(page_load="invalid")  # Invalid type
        timeouts.validate()

def test_invalid_webdriver_config_type():
    """Test invalid WebDriverConfigs type raises TypeError"""
    with pytest.raises(TypeError, match="expected 'headless' to be a bool"):
        config = WebDriverConfigs(headless="invalid")  # Invalid type
        config.validate()
