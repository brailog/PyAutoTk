from controllers.browser.browser_connection import BrowserConnection
from config import logger
import pytest

@pytest.fixture
def browser_connection() -> 'BrowserConnection':
    browser = BrowserConnection()
    logger.info('Browser connection init')
    yield browser
    browser.end()
    logger.info('Browser connection Ended')
