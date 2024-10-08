from typing import Any
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyautotk.core.logger_utils import initialize_logger
from pyautotk.core.config_loader import config

FIREFOX_BIN = "/snap/firefox/current/usr/lib/firefox/firefox"
FIREFOXDRIVE_BIN = "/snap/firefox/current/usr/lib/firefox/geckodriver"

CHROME_BIN = "/usr/bin/google-chrome"


class BrowserController:
    """
    Manages interactions with a web browser using Selenium, providing a high-level API for navigation, element handling,
    and browser control. Supports configurable options such as browser type, headless mode, and maximization.
    """

    def __init__(self, browser_type: str, maximize: bool, headless: bool) -> None:
        """
        Initializes the BrowserController with the specified browser configuration.

        Args:
            browser_type (str): The type of browser to use. Supported values: 'firefox'. Default is 'firefox'.
            maximize (bool): Whether to maximize the browser window on startup. Default is False.
            headless (bool): Whether to run the browser in headless mode. Default is False.
        """
        self.logger = initialize_logger(self.__class__.__name__)
        self.browser_type = browser_type.lower() or config.browser_type
        self.maximize = maximize or config.maximize_browser
        self.headless = headless or config.headless_mode
        self.driver = self._initialize_driver()

    def open_url(self, url: str) -> None:
        """
        Opens the specified URL in the browser.

        Args:
            url (str): The URL to open in the browser.
        """
        self.logger.info(f"Open url: {url} ")
        self.driver.get(url)

    def kill_browser(self) -> None:
        """
        Closes the browser and ends the WebDriver session.
        """
        self.logger.debug("Killing browser session")
        self.driver.quit()

    def find_element(self, xpath: str, timeout: int = 10) -> Any:
        """
        Locates and returns a web element based on the given XPath.

        Args:
            xpath (str): The XPath locator string for the desired element.
            timeout (int): The maximum time (in seconds) to wait for the element to be located. Default is 10 seconds.

        Returns:
            Any: The located WebElement.

        Raises:
            TimeoutException: If the element is not found within the given time.
        """
        self.logger.debug(f"Searching for a element using the following xpath: {xpath}")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def click_element(self, xpath: str, timeout: int = 10) -> None:
        """
        Clicks on the element specified by the given XPath.

        Args:
            xpath (str): The XPath locator string for the element to be clicked.
            timeout (int): The maximum time (in seconds) to wait for the element to be located. Default is 10 seconds.

        Raises:
            TimeoutException: If the element is not found within the given time.
        """
        self.logger.debug(f"Click a element using the following xpath: {xpath}")
        element = self.find_element(xpath, timeout)
        element.click()

    def enter_text(self, xpath: str, text: str, timeout: int = 10) -> None:
        """
        Enters the specified text into a text input field identified by the given XPath.

        Args:
            xpath (str): The XPath locator string for the input field.
            text (str): The text to be entered into the field.
            timeout (int): The maximum time (in seconds) to wait for the element to be located. Default is 10 seconds.

        Raises:
            TimeoutException: If the element is not found within the given time.
        """
        self.logger.debug(f"Enter the following text: {text}")
        element = self.find_element(xpath, timeout)
        element.clear()
        element.send_keys(text)

    def scroll_to_element(self, xpath: str, timeout: int = 10) -> None:
        """
        Scrolls the page until the element identified by the given XPath is in view.

        Args:
            xpath (str): The XPath locator string for the element to scroll to.
            timeout (int): The maximum time (in seconds) to wait for the element to be located. Default is 10 seconds.

        Raises:
            TimeoutException: If the element is not found within the given time.
        """
        self.logger.debug(f"Scrolling to a element using the following xpath: {xpath}")
        element = self.find_element(xpath, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait_for_element(self, xpath: str, timeout: int = 10) -> Any:
        """
        Waits until the element identified by the given XPath is visible.

        Args:
            xpath (str): The XPath locator string for the element to wait for.
            timeout (int): The maximum time (in seconds) to wait for the element to become visible. Default is 10 seconds.

        Returns:
            Any: The WebElement if found and visible, or raises an exception if not found.

        Raises:
            TimeoutException: If the element is not found within the given time.
        """
        self.logger.debug(f"Wait for a element using the following xpath: {xpath}")
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )

    def _initialize_driver(self) -> WebDriver:
        """
        Initializes and returns a Selenium WebDriver instance based on the specified browser configuration.

        Returns:
            WebDriver: The configured Selenium WebDriver instance.

        Raises:
            ValueError: If the specified `browser_type` is not supported.
        """
        self.logger.debug("Init driver")
        if self.browser_type == "firefox":
            options = webdriver.firefox.options.Options()
            options.binary_location = FIREFOX_BIN
            if self.headless:
                options.add_argument("--headless")
            firefox_service = webdriver.firefox.service.Service(executable_path=FIREFOXDRIVE_BIN)
            driver = webdriver.Firefox(service=firefox_service, options=options)
        elif self.browser_type == "chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = CHROME_BIN
            if self.headless:
                chrome_options.add_argument("--headless")

            driver = webdriver.Chrome(options=chrome_options)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")
        if self.maximize:
            driver.maximize_window()

        return driver
