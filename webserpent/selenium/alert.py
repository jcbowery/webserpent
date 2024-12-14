"""Module for alert wrapper"""

from selenium.webdriver.common.alert import Alert as SeleniumAlert

from webserpent.logging.logger import get_system_logger

logger = get_system_logger(__name__)

class Alert:
    """Alert wrapper"""
    def __init__(self, alert: SeleniumAlert):
        self._alert = alert

    @property
    def text(self) -> str:
        """Gets the text of the Alert."""
        logger.info('Getting alert text')
        text = self._alert.text
        logger.debug('Alert text: %s', text)
        return text

    def dismiss(self) -> None:
        """Dismisses the alert available."""
        logger.info('Dismissing the alert')
        try:
            self._alert.dismiss()
            logger.debug('Alert dismissed successfully')
        except Exception as e:
            logger.error('Failed to dismiss alert: %s', e)
            raise

    def accept(self) -> None:
        """Accepts the alert available."""
        logger.info('Accepting the alert')
        try:
            self._alert.accept()
            logger.debug('Alert accepted successfully')
        except Exception as e:
            logger.error('Failed to accept alert: %s', e)
            raise

    def send_keys(self, keys_to_send: str) -> None:
        """Send keys to the Alert.

        :Args:
         - keys_to_send: The text to be sent to Alert.
        """
        logger.info('Sending keys to alert: %s', keys_to_send)
        try:
            self._alert.send_keys(keys_to_send)
            logger.debug('Keys sent to alert successfully')
        except Exception as e:
            logger.error('Failed to send keys to alert: %s', e)
            raise
