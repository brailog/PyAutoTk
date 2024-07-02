from controllers.browser.browser_connection import BrowserConnection
from config import logger


def test_example_one(browser_connection: 'BrowserConnection'):
    browser = browser_connection
    logger.info('Open google page')
    browser.google.open()
    logger.info(browser.driver.title)
    assert browser.driver.title == "Google"
