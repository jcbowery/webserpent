"""Module for base configurations base class"""

from typing import get_type_hints

from webserpent.logging.logger import get_system_logger

logger = get_system_logger(__name__)

class ConfigBase:
    """base class that different configurations inherit from"""
    def validate(self):
        """Validates that the values match the expected values"""
        errors = []
        type_hints = get_type_hints(self)
        for attr, value in self.__dict__.items():
            if type_hints[attr] is not type(value):
                errors.append({attr: type_hints[attr]})
        if errors:
            logger.critical(
                "Error setting %s configs. Incorrect fields with expected value types: %s",
                self,
                errors,
            )
            raise TypeError(
                f"""Error setting {self} configs.
                Incorrect fields with expected value types: {errors}"""
            )
