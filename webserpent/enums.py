"""module holding enums"""

from enum import Enum

class BrowserType(Enum):
    """Enum of supported browser types
    """
    CHROME='chrome'
    FIREFOX='firefox'
    SAFARI='safari'

def string_to_enum(string_value: str, obj):
    """converts a string to the enum object witht hat value

    Args:
        string_value (str)
        obj (_type_): Enum object

    Raises:
        ValueError

    Returns:
        The Enum Object
    """
    try:
        return obj[string_value.upper()]  # Convert string to enum
    except KeyError as e:
        raise ValueError(f"{string_value} is not a valid status") from e
