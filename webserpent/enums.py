"""module holding enums"""

from enum import Enum

class BrowserType(Enum):
    """Enum of supported browser types
    """
    CHROME='chrome'
    FIREFOX='firefox'
    SAFARI='safari'
