from typing import List, Any
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FIREFOX_BIN = "/snap/firefox/current/usr/lib/firefox/firefox"
FIREFOXDRIVE_BIN = "/snap/firefox/current/usr/lib/firefox/geckodriver"

class BrowserController:
    def __init__(self,
                 browser_type: str = 'firefox',
                 maximize: bool = False,
                 headless: bool = False) -> None:
        self.browser_type = browser_type.lower()
        self.maximize = maximize
        self.headless = headless
        self.driver = self._initialize_driver()

    def _initialize_driver(self) -> WebDriver:
        if self.browser_type == 'firefox':
            options = webdriver.firefox.options.Options()
            options.binary_location = FIREFOX_BIN
            if self.headless:
                options.add_argument('--headless')

            firefox_service = webdriver.firefox.service.Service(executable_path=FIREFOXDRIVE_BIN)
            driver = webdriver.Firefox(service=firefox_service, options=options)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")
        if self.maximize:
            driver.maximize_window()
        return driver

    def open_url(self, url: str) -> None:
        self.driver.get(url)

    def kill_browser(self) -> None:
        self.driver.quit()

    def find_element(self, xpath: str, timeout: int = 10) -> Any:
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def click_element(self, xpath: str, timeout: int = 10) -> None:
        element = self.find_element(xpath, timeout)
        element.click()

    def enter_text(self, xpath: str, text: str, timeout: int = 10) -> None:
        element = self.find_element(xpath, timeout)
        element.clear()
        element.send_keys(text)

    def scroll_to_element(self, xpath: str, timeout: int = 10) -> None:
        element = self.find_element(xpath, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait_for_element(self, xpath: str, timeout: int = 10) -> Any:
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
