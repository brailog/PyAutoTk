from controllers.browser.browser_controller import BrowserController
from config import logger


def test_example_one(browser_controller: 'BrowserController'):
    browser = browser_controller
    logger.info('Open google page')
    browser.open_url("https://www.google.com")
    logger.info(browser.driver.title)
    assert browser.driver.title == "Google"
