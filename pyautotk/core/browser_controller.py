import os
import time
from typing import Any
from platform import system
from playwright.sync_api import sync_playwright, Page, Locator

from pyautotk.core.logger_utils import initialize_logger
from pyautotk.core.config_loader import config
from pyautotk.core.exceptions import BrowserWaitForPageLoadException

class BrowserController:
    """
    Manages interactions with a web browser using Playwright, providing a high-level API for navigation, element handling,
    and browser control. Supports configurable options such as browser type, headless mode, and maximization.
    """

    def __init__(self, browser_type: str = "chromium", maximize: bool = False, headless: bool = False) -> None:
        """
        Initializes the BrowserController with Playwright.

        Args:
            browser_type (str): The type of browser to use. Supported values: 'chromium', 'firefox', 'webkit'. Default is 'chromium'.
            maximize (bool): Whether to maximize the browser window on startup. Default is False.
            headless (bool): Whether to run the browser in headless mode. Default is False.
        """
        self.logger = initialize_logger(self.__class__.__name__)
        self.browser_type = browser_type or config.browser_type
        self.headless = headless or config.headless_mode
        self.maximize = maximize or config.maximize_browser
        self.playwright = sync_playwright().start()
        self.browser = self._initialize_browser()
        self.page = self.browser.new_page()

    def _initialize_browser(self):
        """Initializes Playwright's browser based on configuration."""
        self.logger.debug(f"Starting {self.browser_type} browser")
        return getattr(self.playwright, self.browser_type).launch(headless=self.headless)

    def wait_for_initial_load(self, timeout: int = 15, init_sleep_time: int = 3) -> None:
        """
        Waits for the page to fully load by checking document readiness.

        Args:
            timeout (int): Maximum time to wait for the page to load, in seconds.
            init_sleep_time (int): Fixed sleep time before initiating wait checks, in seconds.

        Raises:
            BrowserWaitForPageLoadException: If the page does not fully load within the timeout.
        """
        self.logger.info(f"Waiting for page load with a timeout of {timeout} seconds")
        time.sleep(init_sleep_time)
        try:
            self.page.wait_for_load_state("load", timeout=timeout * 1000)
        except Exception:
            raise BrowserWaitForPageLoadException(timeout)

    def open_url(self, url: str) -> None:
        """Opens a URL in the browser."""
        self.logger.info(f"Opening URL: {url}")
        self.page.goto(url, wait_until="load")

    def close_browser(self) -> None:
        """Closes the browser session."""
        self.logger.debug("Closing browser session")
        self.browser.close()
        self.playwright.stop()

    def find_element(self, selector: str, timeout: int = 10) -> Locator:
        """
        Locates and returns a web element.

        Args:
            selector (str): CSS or XPath selector.
            timeout (int): Maximum time (in seconds) to wait for the element.

        Returns:
            Locator: The located element.
        """
        self.logger.debug(f"Finding element with selector: {selector}")
        return self.page.wait_for_selector(selector, timeout=timeout * 1000)

    def click_element(self, selector: str, timeout: int = 10) -> None:
        """
        Clicks on an element.

        Args:
            selector (str): CSS or XPath selector.
            timeout (int): Maximum time (in seconds) to wait for the element.
        """
        self.logger.debug(f"Clicking element: {selector}")
        element = self.find_element(selector, timeout)
        element.click()

    def enter_text(self, selector: str, text: str, timeout: int = 10) -> None:
        """
        Enters text into an input field.

        Args:
            selector (str): CSS or XPath selector.
            text (str): The text to enter.
            timeout (int): Maximum time (in seconds) to wait for the element.
        """
        self.logger.debug(f"Entering text '{text}' into element: {selector}")
        element = self.find_element(selector, timeout)
        element.fill(text)

    def scroll_to_element(self, selector: str, timeout: int = 10) -> None:
        """
        Scrolls the page until the element is in view.

        Args:
            selector (str): CSS or XPath selector.
            timeout (int): Maximum time (in seconds) to wait for the element.
        """
        self.logger.debug(f"Scrolling to element: {selector}")
        element = self.find_element(selector, timeout)
        element.scroll_into_view_if_needed()

    def wait_for_element(self, selector: str, timeout: int = 10) -> None:
        """
        Waits until an element is visible.

        Args:
            selector (str): CSS or XPath selector.
            timeout (int): Maximum time (in seconds) to wait.
        """
        self.logger.debug(f"Waiting for element: {selector}")
        self.page.wait_for_selector(selector, state="visible", timeout=timeout * 1000)

    def hover_element(self, selector: str, timeout: int = 10) -> None:
        """
        Hovers over an element.

        Args:
            selector (str): CSS or XPath selector.
            timeout (int): Maximum time (in seconds) to wait.
        """
        self.logger.debug(f"Hovering over element: {selector}")
        element = self.find_element(selector, timeout)
        element.hover()

    def get_text(self, selector: str, timeout: int = 10) -> str:
        """
        Retrieves the text content of an element.

        Args:
            selector (str): CSS or XPath selector.
            timeout (int): Maximum time (in seconds) to wait.

        Returns:
            str: The text content of the element.
        """
        self.logger.debug(f"Getting text from element: {selector}")
        element = self.find_element(selector, timeout)
        return element.inner_text()

    def get_attribute(self, selector: str, attribute_name: str, timeout: int = 10) -> str:
        """
        Retrieves the value of a specific attribute from an element.

        Args:
            selector (str): CSS or XPath selector.
            attribute_name (str): The attribute to retrieve.
            timeout (int): Maximum time (in seconds) to wait.

        Returns:
            str: The value of the specified attribute.
        """
        self.logger.debug(f"Getting attribute '{attribute_name}' from element: {selector}")
        element = self.find_element(selector, timeout)
        return element.get_attribute(attribute_name)
