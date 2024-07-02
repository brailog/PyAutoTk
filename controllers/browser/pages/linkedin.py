from controllers.browser.pages.abc_pages import PageObj
from controllers.browser.widget import Widget
from selenium.webdriver.remote.webdriver import WebDriver


class Linkedin(PageObj):
    def __init__(self, browser_driver: 'WebDriver'):
        self._driver = browser_driver
        self.URL = "https://www.linkedin.com/"
        self._btn_username_login = Widget(self._driver, id="username", name="session_key", type="text")
        self._btn_password_login = Widget(self._driver, id="password", name="session_password", type="password")
        self._btn_login = Widget(self._driver, text="Sign in")
        self._btn_login_submit = Widget(self._driver, text="Sign in", type="submit")

    def open(self):
        self._driver.get(self.URL)

    def in_home_page_do_login(self, email_account: str, password: str):
        self._btn_login.click()
        self._btn_username_login.click()
        self._btn_username_login.enter_text(email_account)
        self._btn_password_login.click()
        self._btn_password_login.enter_text(password)
        self._btn_login_submit.click()
