from controllers.browser.browser_controller import BrowserController
from config import logger
import pytest

@pytest.fixture
def browser_controller() -> 'BrowserController':
    browser = BrowserController()
    logger.info('Browser Controller init')
    yield browser
    browser.end()
    logger.info('Browser Controller Ended')
