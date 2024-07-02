import pytest
from controllers.browser.browser_controller import BrowserController
from controllers.browser.widget import Widget


def test_example_one(browser_controller: 'BrowserController'):
    browser = browser_controller
    browser.open_url("https://www.linkedin.com/")

    btn_login = Widget(browser.driver, text="Sign in")
    btn_username_login = Widget(browser.driver, id="username", name="session_key", type="text")
    btn_password_login = Widget(browser.driver, id="password", name="session_password", type="password")
    btn_login.click()
    btn_username_login.click()
    btn_username_login.enter_text(pytest.email_account_test)
    btn_password_login.click()
    btn_password_login.enter_text(pytest.password_account_test)
    btn_login = Widget(browser.driver, text="Sign in", type="submit")
    btn_login.click()
