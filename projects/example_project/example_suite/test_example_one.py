import pytest
from config import logger
from controllers.browser.browser_connection import BrowserConnection


def test_example_one(browser_connection: 'BrowserConnection') -> None:
    browser_connection.linkedin.open()
    browser_connection.linkedin.in_home_page_do_login(pytest.email_account_test,
                                                      pytest.password_account_test
                                                      )
    assert "Feed" in browser_connection.driver.title

