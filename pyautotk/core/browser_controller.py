import os
from typing import Any
from platform import system
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

from pyautotk.core.logger_utils import initialize_logger
from pyautotk.core.config_loader import config

FIREFOX_BIN_LINUX = os.path.join("/snap", "firefox", "current", "usr", "lib", "firefox", "firefox")
FIREFOXDRIVE_BIN_LINUX = os.path.join("/snap", "firefox", "current", "usr", "lib", "firefox", "geckodriver")
CHROME_BIN_LINUX = os.path.join("/usr", "bin", "google-chrome")

FIREFOX_BIN_WINDOWS = os.path.join("C:\\", "Program Files", "Mozilla Firefox", "firefox.exe")
CHROME_BIN_WINDOWS = os.path.join("C:\\", "Program Files", "Google", "Chrome", "Application", "chrome.exe")


class BrowserController:
    """
    Manages interactions with a web browser using Selenium, providing a high-level API for navigation, element handling,
    and browser control. Supports configurable options such as browser type, headless mode, and maximization.
    """

    def __init__(self, browser_type: str, maximize: bool, headless: bool, kill_browser: bool = True) -> None:
        """
        Initializes the BrowserController with the specified browser configuration.

        Args:
            browser_type (str): The type of browser to use. Supported values: 'firefox' and 'chrome'. Default is 'firefox'.
            maximize (bool): Whether to maximize the browser window on startup. Default is False.
            headless (bool): Whether to run the browser in headless mode. Default is False.
        """
        self.logger = initialize_logger(self.__class__.__name__)
        self.os_type = system()
        self.browser_type = browser_type.lower() or config.browser_type
        self.maximize = maximize or config.maximize_browser
        self.headless = headless or config.headless_mode
        self.kill_browser = kill_browser
        self.driver = self._initialize_driver()
        self.original_window = self.driver.current_window_handle
        print(self.original_window)

    def open_url(self, url: str) -> None:
        """
        Opens the specified URL in the browser.

        Args:
            url (str): The URL to open in the browser.
        """
        self.logger.info(f"Open url: {url} ")
        self.driver.get(url)

    def close_browser(self) -> None:
        """
        Closes the browser and ends the WebDriver session.
        """
        self.logger.debug("Killing browser session")
        self.driver.quit()

    def accept_alert(self, timeout: int = 5) -> None:
        """
        Waits for and accepts a JavaScript alert.

        Args:
            timeout (int): The maximum time in seconds to wait for the alert.

        Raises:
            TimeoutException: If no alert is present within the timeout period.
        """
        try:
            self.logger.debug(f"Waiting for alert for {timeout} seconds.")
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            self.logger.info(f"Accepting alert with text: '{alert_text}'")
            alert.accept()
            self.driver.switch_to.default_content()
        except TimeoutException:
            self.logger.error(f"No alert was present within {timeout} seconds.")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while handling the alert: {e}")
            raise

    def switch_to_new_tab(self) -> None:
        """
        Switches the driver's focus to the most recently opened tab/window.
        It assumes the new tab is the last one in the list of window handles.
        """
        self.logger.debug("Attempting to switch to the new tab.")
        all_handles = self.driver.window_handles
        if len(all_handles) > 1:
            new_tab_handle = all_handles[-1]
            self.driver.switch_to.window(new_tab_handle)
            self.logger.info(f"Switched to new tab with handle: {new_tab_handle}")
        else:
            self.logger.warning("No new tab to switch to. Only one tab is open.")

    def switch_to_original_tab(self) -> None:
        """
        Switches the driver's focus back to the original tab/window that was open
        when the BrowserController was instantiated. If the original tab is closed,
        it switches to the first available tab.
        """
        self.logger.debug("Switching back to the original tab.")
        try:
            self.driver.switch_to.window(self.original_window)
            self.logger.info(f"Switched back to original tab with handle: {self.original_window}")
        except NoSuchWindowException:
            self.logger.warning("Original tab seems to be closed. Switching to the first available tab.")
            if self.driver.window_handles:
                self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                self.logger.error("No tabs available to switch to. The browser might be closed.")

    def close_current_tab(self) -> None:
        """
        Closes the currently focused tab and switches back to the original tab.
        If only one tab is open, it will not be closed.
        """
        self.logger.debug(f"Attempting to close the current tab.")
        if len(self.driver.window_handles) > 1:
            self.driver.close()
            self.switch_to_original_tab()
        else:
            self.logger.warning("Cannot close the tab as it is the only one open. Use `close_browser()` to end the session.")

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
        self.wait_for_element(xpath)
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
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
        self.driver.execute_script("arguments[0].click();", element)

    def hover_element(self, xpath: str, timeout: int = 10) -> None:
        element = self.find_element(xpath, timeout)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def unhover_element(self, timeout: int = 10) -> None:
        """
        Moves the mouse to a neutral area (the <body> tag) to un-hover any active element.

        Args:
            timeout (int): Maximum time to wait for the body element to be present.
        """
        self.logger.debug("Unhovering by moving mouse to the body element.")
        try:
            body_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            ActionChains(self.driver).move_to_element(body_element).perform()
        except Exception as e:
            self.logger.error(f"Failed to move mouse to body element to unhover. Error: {e}")
            raise

    def drag_and_drop(self, source_xpath: str, target_xpath: str, timeout: int = 10) -> None:
        """
        Performs a drag-and-drop action from a source element to a target element.

        Args:
            source_xpath (str): The XPath locator for the element to drag.
            target_xpath (str): The XPath locator for the element to drop onto.
            timeout (int): Maximum time to wait for the elements.
        """
        self.logger.debug(f"Performing drag and drop from '{source_xpath}' to '{target_xpath}'.")
        try:
            source_element = self.find_element(source_xpath, timeout)
            target_element = self.find_element(target_xpath, timeout)
            ActionChains(self.driver).drag_and_drop(source_element, target_element).perform()
            self.logger.info("Drag and drop action completed successfully.")
        except Exception as e:
            self.logger.error(f"Drag and drop action failed. Error: {e}")
            raise

    def enter_text_safely(self, xpath: str, text: str, timeout: int = 10) -> None:
        """
        Enters the specified text into a text input field safely by focusing on the element before interacting.

        Args:
            xpath (str): The XPath locator string for the input field.
            text (str): The text to be entered into the field.
            timeout (int): Maximum time (in seconds) to wait for the element to be located. Default is 10 seconds.

        Raises:
            TimeoutException: If the element is not found within the given time.
        """
        self.logger.debug(f"Enter text safely: {text} into element with XPath: {xpath}")
        element = self.find_element(xpath, timeout)
        
        self.driver.execute_script("arguments[0].focus();", element)
        
        element.clear()
        element.send_keys(text)

    def set_element_value(self, xpath: str, value: str, timeout: int = 10) -> None:
        """
        Sets the value of an element directly using JavaScript.
        This is particularly useful for sliders or other inputs where send_keys is not reliable.

        Args:
            xpath (str): The XPath locator string for the element.
            value (str): The value to set for the element.
            timeout (int): Maximum time (in seconds) to wait for the element to be located.
        """
        self.logger.debug(f"Setting value '{value}' for element with XPath: {xpath} using JavaScript.")
        element = self.find_element(xpath, timeout)
        # Set the value and then dispatch a 'change' event to ensure any listeners are triggered.
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
            element,
            value
        )

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

    def wait_for_all_elements(self, xpath: str, timeout: int = 10) -> list:
        """
        Waits until all elements identified by the given XPath are visible.

        Args:
            xpath (str): The XPath locator string for the elements to wait for.
            timeout (int): The maximum time (in seconds) to wait for the elements to become visible. Default is 10 seconds.

        Returns:
            list: A list of WebElement objects if found and visible, or raises an exception if not found.

        Raises:
            TimeoutException: If no elements are found or visible within the given time.
        """
        self.logger.debug(f"Wait for all elements using the following xpath: {xpath}")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )

    def upload_file(self, xpath: str, file_path: str, timeout: int = 10) -> None:
        """
        Uploads a file by sending the file path to a file input element.

        Args:
            xpath (str): The XPath locator string for the file input element.
            file_path (str): The absolute path to the file to be uploaded.
            timeout (int): Maximum time (in seconds) to wait for the element to be present. Default is 10 seconds.

        Raises:
            FileNotFoundError: If the file specified by file_path does not exist.
            TimeoutException: If the element is not present within the given time.
            ValueError: If the provided file_path is not an absolute path.
        """
        self.logger.debug(f"Uploading file '{file_path}' to element with XPath: {xpath}")
        if not os.path.isabs(file_path):
            raise ValueError("File path for upload must be an absolute path.")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file to upload was not found at: {file_path}")

        # We wait for presence, not visibility, as file inputs can be hidden for styling.
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        element.send_keys(file_path)

    def _get_select_object(self, xpath: str, timeout: int = 10) -> Select:
        """Finds a <select> element and returns a Select object."""
        element = self.find_element(xpath, timeout)
        return Select(element)

    def select_option_by_text(self, xpath: str, text: str, timeout: int = 10) -> None:
        """
        Selects an option from a dropdown by its visible text.

        Args:
            xpath (str): The XPath locator for the <select> element.
            text (str): The visible text of the option to select.
            timeout (int): Maximum time to wait for the element.
        """
        self.logger.debug(f"Selecting option '{text}' by text from dropdown with XPath: {xpath}")
        select = self._get_select_object(xpath, timeout)
        select.select_by_visible_text(text)

    def select_option_by_value(self, xpath: str, value: str, timeout: int = 10) -> None:
        """
        Selects an option from a dropdown by its 'value' attribute.

        Args:
            xpath (str): The XPath locator for the <select> element.
            value (str): The value attribute of the option to select.
            timeout (int): Maximum time to wait for the element.
        """
        self.logger.debug(f"Selecting option with value '{value}' from dropdown with XPath: {xpath}")
        select = self._get_select_object(xpath, timeout)
        select.select_by_value(value)

    def select_option_by_index(self, xpath: str, index: int, timeout: int = 10) -> None:
        """
        Selects an option from a dropdown by its index.

        Args:
            xpath (str): The XPath locator for the <select> element.
            index (int): The index of the option to select (0-based).
            timeout (int): Maximum time to wait for the element.
        """
        self.logger.debug(f"Selecting option at index {index} from dropdown with XPath: {xpath}")
        select = self._get_select_object(xpath, timeout)
        select.select_by_index(index)

    def deselect_all_options(self, xpath: str, timeout: int = 10) -> None:
        """
        Deselects all options in a multi-select dropdown.

        Args:
            xpath (str): The XPath locator for the <select> element.
            timeout (int): Maximum time to wait for the element.
        """
        self.logger.debug(f"Deselecting all options from dropdown with XPath: {xpath}")
        select = self._get_select_object(xpath, timeout)
        if select.is_multiple:
            select.deselect_all()
        else:
            self.logger.warning("Deselect_all is only applicable to multi-select dropdowns.")

    def deselect_option_by_text(self, xpath: str, text: str, timeout: int = 10) -> None:
        """
        Deselects an option from a multi-select dropdown by its visible text.

        Args:
            xpath (str): The XPath locator for the <select> element.
            text (str): The visible text of the option to deselect.
            timeout (int): Maximum time to wait for the element.
        """
        self.logger.debug(f"Deselecting option '{text}' by text from dropdown with XPath: {xpath}")
        select = self._get_select_object(xpath, timeout)
        if select.is_multiple:
            select.deselect_by_visible_text(text)
        else:
            self.logger.warning("Deselection is only applicable to multi-select dropdowns.")

    def get_all_selected_options_text(self, xpath: str, timeout: int = 10) -> list[str]:
        """
        Gets the text of all selected options from a dropdown.

        Args:
            xpath (str): The XPath locator for the <select> element.
            timeout (int): Maximum time to wait for the element.
        """
        select = self._get_select_object(xpath, timeout)
        return [option.text for option in select.all_selected_options]

    def _initialize_driver(self) -> WebDriver:
        """
        Initializes and returns a Selenium WebDriver instance based on the specified browser configuration.

        Returns:
            WebDriver: The configured Selenium WebDriver instance.

        Raises:
            ValueError: If the specified `browser_type` is not supported.
        """
        self.logger.debug("Init driver")

        if self.os_type == "Windows":
            firefox_bin = FIREFOX_BIN_WINDOWS
            firefox_driver_bin = ""
            chrome_bin = CHROME_BIN_WINDOWS
        else:
            firefox_bin = FIREFOX_BIN_LINUX
            firefox_driver_bin = FIREFOXDRIVE_BIN_LINUX
            chrome_bin = CHROME_BIN_LINUX

        if self.browser_type == "firefox":
            options = webdriver.firefox.options.Options()
            options.binary_location = firefox_bin
            options.add_experimental_option("detach", not self.kill_browser)
            if self.headless:
                options.add_argument("--headless")

            firefox_service = FirefoxService(executable_path=firefox_driver_bin)
            driver = webdriver.Firefox(service=firefox_service, options=options)

        elif self.browser_type == "chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = chrome_bin
            chrome_options.add_experimental_option("detach", not self.kill_browser)
            if self.headless:
                chrome_options.add_argument("--headless")

            chrome_service = ChromeService()
            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        if self.maximize:
            driver.maximize_window()

        return driver
