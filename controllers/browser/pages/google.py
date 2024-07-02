from controllers.browser.pages.abc_pages import PageObj
from selenium.webdriver.remote.webdriver import WebDriver


class Google(PageObj):
    def __init__(self, browser_driver: 'WebDriver'):
        self._driver = browser_driver
        self.URL = "https://www.google.com/"

    def open(self):
        self._driver.get(self.URL)
