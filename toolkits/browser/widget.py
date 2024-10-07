import re
from typing import Dict, Any
from selenium.webdriver.remote.webelement import WebElement
from .input import Input

class Widget:
    def __init__(self, controller, **kwargs: str) -> None:
        self.controller = controller
        self.attrs = kwargs
        self.xpath = self._build_xpath()

    def _build_xpath(self) -> str:
        xpath = "//*"
        conditions = []

        for attr, value in self.attrs.items():
            attr = re.sub(r'_', '-', attr)
            if attr == 'text':
                conditions.append(f"contains(text(), '{value}')")
            elif 'class-' in attr:
                conditions.append(f"@class='{value}'")
            else:
                conditions.append(f"@{attr}='{value}'")

        if conditions:
            xpath += "[" + " and ".join(conditions) + "]"
        return xpath

    def _build_fallback_xpath(self) -> str:
        xpath = "//*"
        conditions = []

        for attr, value in self.attrs.items():
            attr = re.sub(r'_', '-', attr)
            if attr == 'text':
                conditions.append(f"contains(text(), '{value}')")
            else:
                conditions.append(f"contains(@{attr}, '{value}')")

        if conditions:
            xpath += "[" + " and ".join(conditions) + "]"

        return xpath

    def click(self, timeout=10) -> None:
        self.controller.click_element(self.xpath, timeout)

    def enter_text(self, text: str, timeout: int = 10) -> None:
        self.click()
        self.controller.enter_text(self.xpath, text, timeout)

    def scroll_to(self, timeout: int = 10) -> None:
        self.controller.scroll_to_element(self.xpath, timeout)

    def wait_for(self, timeout: int = 10) -> Any:
        return self.controller.wait_for_element(self.xpath, timeout)

    @staticmethod
    def get_all_elements_with_attribute(controller, attribute: str) -> Dict[str, WebElement]:
        return controller.find_elements(f"//*[@{attribute}]")
