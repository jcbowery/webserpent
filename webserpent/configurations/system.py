"""Module for system config data class"""

from dataclasses import dataclass

from webserpent.configurations.configs_base import ConfigBase
from webserpent.logging.logger import get_system_logger

logger = get_system_logger(__name__)


@dataclass
class SystemConfigs(ConfigBase):
    """Settings for the Test System"""

    log_level: int = 10
    log_dir_path: str = "Logs"
    page_dir_path: str = "Pages"
    binary_dir_path: str = ""
