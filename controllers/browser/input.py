from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class Input:
    def __init__(self, element: WebElement) -> None:
        self.element = element

    def press_enter(self) -> None:
        self.element.send_keys(Keys.ENTER)

    def press_escape(self) -> None:
        self.element.send_keys(Keys.ESCAPE)

    def press_tab(self) -> None:
        self.element.send_keys(Keys.TAB)

    def send_keys(self, keys: str) -> None:
        self.element.send_keys(keys)
