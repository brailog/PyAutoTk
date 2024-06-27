import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Any, Dict
from .input import Input


class Widget:
    def __init__(self, driver: WebDriver, **kwargs: str) -> None:
        self.driver = driver
        self.attrs = kwargs
        self.xpath = self._build_xpath()

    def _build_xpath(self) -> str:
        xpath = "//*"
        conditions = []

        for attr, value in self.attrs.items():
            attr = re.sub(r'_', '-', attr)
            if attr == 'text':
                conditions.append(f"contains(text(), '{value}')")
            elif 'class' in attr:
                conditions.append(f"@class='{value}'")
            else:
                conditions.append(f"@{attr}='{value}'")

        if conditions:
            xpath += "[" + " and ".join(conditions) + "]"
        print(xpath)
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

    def find(self, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, self.xpath)))
        except:
            fallback_xpath = self._build_fallback_xpath()
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, fallback_xpath)))

    def click(self, timeout=10):
        element = self.find(timeout)
        element.click()

    def enter_text(self, text: str, timeout: int = 10) -> None:
        element = self.find(timeout)
        element.clear()
        element.send_keys(text)

    def scroll_to(self, timeout: int = 10) -> None:
        element = self.find(timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait_for(self, condition: Any, timeout: int = 10) -> Any:
        return WebDriverWait(self.driver, timeout).until(condition((By.XPATH, self.xpath)))

    @staticmethod
    def get_all_elements_with_attribute(driver: WebDriver, attribute: str) -> Dict[str, WebElement]:
        elements = driver.find_elements(By.XPATH, f"//*[@{attribute}]")
        element_dict = {element.get_attribute(attribute): element for element in elements}
        return element_dict

    @property
    def get_input(self) -> 'Input':
        element = self.find()
        return Input(element)
