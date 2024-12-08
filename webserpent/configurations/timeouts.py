"""Module for timeout configs"""

from dataclasses import dataclass
from webserpent.configurations.configs_base import ConfigBase

@dataclass
class TimeOuts(ConfigBase):
    """Time out configurations"""
    implicit: int = 0
    page_load: int = 30
    find_element: int = 5
    element_interaction: int = 2

