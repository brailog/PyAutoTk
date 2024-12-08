from pyautotk.elements.helpers.session_helpers import browser_session
from pyautotk.elements.widget import Widget
from unittest.mock import MagicMock
import unittest
import psutil


GOOGLE_URL = "https://www.google.com/"

def _get_current_browser_process_number(process_name):
    return sum(1 for proc in psutil.process_iter(['name']) if process_name in proc.info['name'].lower())


class TestBrowserSessionInit(unittest.TestCase):
    def setUp(self):
        self.controller = MagicMock()
        self.chrome_name = "chrome"
        self.firefox_browser = "firefox"
        self.init_chrome_process_number = _get_current_browser_process_number(self.chrome_name)
        self.init_firefox_process = _get_current_browser_process_number(self.firefox_browser)

    def test_chrome_browser_session(self):
        @browser_session(GOOGLE_URL)
        def _test_chrome_browser_session(session):
            assert _get_current_browser_process_number(self.chrome_name) > self.init_chrome_process_number
        _test_chrome_browser_session()

    def test_firefix_browser_session(self):
        @browser_session(GOOGLE_URL, browser_type=self.firefox_browser)
        def _test_firefox_browser_session(session):
            assert _get_current_browser_process_number(self.firefox_browser) > self.init_firefox_process
        _test_firefox_browser_session()


class TestBrowserSessionHeadless(unittest.TestCase):
    def setUp(self):
        self.controller = MagicMock()
        self.chrome_name = "chrome"
        self.firefox_browser = "firefox"
        self.init_chrome_process_number = _get_current_browser_process_number(self.chrome_name)
        self.init_firefox_process = _get_current_browser_process_number(self.firefox_browser)

    def test_chrome_browser_headless(self):
        @browser_session(GOOGLE_URL, headless=True)
        def _test_chrome_browser_headless(session):
            assert session.driver.title == "Google"
        _test_chrome_browser_headless()

    def test_firefox_browser_headless(self):
        @browser_session(GOOGLE_URL, headless=True)
        def _test_firefox_browser_headless(session):
            assert session.driver.title == "Google"
        _test_firefox_browser_headless()

if __name__ == '__main__':
    unittest.main()
