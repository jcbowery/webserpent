from pytest_mock import MockerFixture
from webserpent.logging.logger import get_system_logger

def test_get_system_logger_with_env_var(mocker: MockerFixture):
    mock_system_logger = mocker.Mock()
    mocker.patch('webserpent.logging.logger._setup_system_logger', return_value=mock_system_logger)
    mocker.patch.dict("os.environ", {"ENV": "dev"})
    
    x = get_system_logger('my_name')

    assert x == mock_system_logger

def test_get_system_logger_without_env_var(mocker: MockerFixture):
    mock_system_logger = mocker.Mock()
    mock_blank_logger = mocker.Mock()
    mocker.patch('webserpent.logging.logger._setup_system_logger', return_value=mock_system_logger)
    mocker.patch('webserpent.logging.logger._blank_logger', return_value=mock_blank_logger)
    mocker.patch.dict("os.environ", {"ENV": "prod"})
    
    x = get_system_logger('my_name')

    assert x == mock_blank_logger

