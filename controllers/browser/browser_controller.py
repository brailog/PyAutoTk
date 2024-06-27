from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class BrowserController:
    def __init__(self, browser_type: str = 'firefox') -> None:
        self.browser_type = browser_type.lower()
        self.driver = self._initialize_driver()

    def _initialize_driver(self) -> WebDriver:
        if self.browser_type == 'chrome':
            driver = webdriver.Chrome()
        elif self.browser_type == 'firefox':
            driver = webdriver.Firefox()
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        driver.maximize_window()
        return driver

    def open_url(self, url: str) -> None:
        self.driver.get(url)

    def close_browser(self) -> None:
        self.driver.quit()
