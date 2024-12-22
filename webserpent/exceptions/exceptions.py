"""Module for Custom Exceptions"""

class FailureException(Exception):
    """Base exception for failure scenarios."""


class FlakyException(Exception):
    """Base exception for flaky scenarios."""


class UnexpectedException(Exception):
    """Base exception for unexpected scenarios."""


class ClickFailureException(FailureException):
    """Exception for failures during click actions."""


class FlakyClickException(FlakyException):
    """Exception for flaky behavior during click actions."""


class UnexpectedClickException(UnexpectedException):
    """Exception for unexpected issues during click actions."""

class FlakySendTetxException(FlakyException):
    """Excepeting for flaky behavior during a send text action"""

class SendTextFailureException(FailureException):
    """Exception for failure during send text"""

class UnexptedSendTextException(UnexpectedException):
    """Exception for unexpected issues during send keys action"""
