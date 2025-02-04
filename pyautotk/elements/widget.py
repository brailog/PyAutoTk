import re
import time
from typing import Dict, Any, List
from pyautotk.core.logger_utils import initialize_logger
from pyautotk.core.exceptions import (
    WidgetWaitTimeoutException,
    WidgetClickException,
    WidgetDoubleClickException,
    WidgetHoverException,
    WidgetEnterTextException,
    WidgetScrollException,
    WidgetRetrievePropertiesException,
    WidgetAttributeException,
    WidgetExtractionException,
)

class Widget:
    """
    Base class for UI elements, providing generic interaction methods.
    """

    def __init__(self, controller: Any, selector: str) -> None:
        self.logger = initialize_logger(self.__class__.__name__)
        self.controller = controller
        self.selector = selector

    def click(self, timeout: int = 10) -> None:
        """Clicks the element."""
        try:
            self.controller.click_element(self.selector, timeout)
        except Exception as e:
            raise WidgetClickException(self.selector, e)

    def double_click(self, timeout: int = 10) -> None:
        """Performs a double-click on the element."""
        try:
            self.controller.page.dblclick(self.selector, timeout=timeout * 1000)
        except Exception as e:
            raise WidgetDoubleClickException(self.selector, e)

    def hover(self, timeout: int = 10) -> None:
        """Simulates a mouse hover action."""
        try:
            self.controller.hover_element(self.selector, timeout)
        except Exception as e:
            raise WidgetHoverException(self.selector, e)

    def enter_text(self, text: str, timeout: int = 10) -> None:
        """Enters text into the element."""
        try:
            self.controller.enter_text(self.selector, text, timeout)
        except Exception as e:
            raise WidgetEnterTextException(self.selector, e)

    def scroll_to(self, timeout: int = 10) -> None:
        """Scrolls to the element."""
        try:
            self.controller.scroll_to_element(self.selector, timeout)
        except Exception as e:
            raise WidgetScrollException(self.selector, e)

    def wait_for(self, timeout: int = 10) -> None:
        """Waits until the element is visible."""
        try:
            self.controller.wait_for_element(self.selector, timeout)
        except Exception as e:
            raise WidgetWaitTimeoutException(self.selector, timeout, e)

    def get_attribute(self, attribute_name: str, timeout: int = 10) -> str:
        """Retrieves the value of a specific attribute from the element."""
        try:
            return self.controller.get_attribute(self.selector, attribute_name, timeout)
        except Exception as e:
            raise WidgetAttributeException(self.selector, e)

    def get_text(self, timeout: int = 10) -> str:
        """Retrieves the inner text of the element."""
        try:
            return self.controller.get_text(self.selector, timeout)
        except Exception as e:
            raise WidgetRetrievePropertiesException(self.selector, e)


# ----------- CLASSES FILHAS ESPECÍFICAS ----------- #

class Button(Widget):
    """Represents a Button element."""

    def __init__(self, controller: Any, **kwargs: str):
        selector = f"button[{self._build_selector(kwargs)}], input[type='submit'][{self._build_selector(kwargs)}], input[type='button'][{self._build_selector(kwargs)}]"
        super().__init__(controller, selector)

    def _build_selector(self, attrs: Dict[str, str]) -> str:
        """Builds a Playwright CSS selector based on attributes."""
        return "][".join([f"{key}='{value}'" for key, value in attrs.items()]) if attrs else ""


import re
from pyautotk.elements.widget import Widget

class SearchBar(Widget):
    """Represents a Search Bar inside Web Components like the Reddit search bar."""

    def __init__(self, controller: Any, **kwargs: str):
        """
        Inicializa um SearchBar.

        Args:
            controller (Any): O controlador do navegador Playwright.
            kwargs (str): Atributos para construção do seletor.
        """
        selector = f"faceplate-search-input[{self._build_selector(kwargs)}]"
        super().__init__(controller, selector)

    def _build_selector(self, attrs: Dict[str, str]) -> str:
        """Constrói um seletor CSS baseado nos atributos fornecidos."""
        return "][".join([f"{key}='{value}'" for key, value in attrs.items()]) if attrs else ""

    def click(self, timeout: int = 10) -> None:
        """Clica no campo de busca dentro do Web Component."""
        try:
            # Acessa o input dentro do Shadow DOM
            shadow_input = self.controller.page.locator(self.selector).locator("input")
            shadow_input.click(timeout=timeout * 1000)
        except Exception as e:
            raise WidgetClickException(self.selector, e)

    def enter_text(self, text: str, timeout: int = 10) -> None:
        """Entra com um texto no campo de busca."""
        try:
            shadow_input = self.controller.page.locator(self.selector).locator("input")
            shadow_input.fill(text, timeout=timeout * 1000)
        except Exception as e:
            raise WidgetEnterTextException(self.selector, e)

    def press_enter(self, timeout: int = 10) -> None:
        """Pressiona a tecla Enter após inserir um texto."""
        try:
            shadow_input = self.controller.page.locator(self.selector).locator("input")
            shadow_input.press("Enter", timeout=timeout * 1000)
        except Exception as e:
            raise WidgetEnterTextException(self.selector, e)


class Checkbox(Widget):
    """Represents a Checkbox element."""

    def __init__(self, controller: Any, **kwargs: str):
        selector = f"input[type='checkbox'][{self._build_selector(kwargs)}]"
        super().__init__(controller, selector)

    def _build_selector(self, attrs: Dict[str, str]) -> str:
        return "][".join([f"{key}='{value}'" for key, value in attrs.items()]) if attrs else ""

    def is_checked(self, timeout: int = 10) -> bool:
        """Checks if the checkbox is selected."""
        return self.controller.page.locator(self.selector).is_checked()


class RadioButton(Widget):
    """Represents a Radio Button element."""

    def __init__(self, controller: Any, **kwargs: str):
        selector = f"input[type='radio'][{self._build_selector(kwargs)}]"
        super().__init__(controller, selector)

    def _build_selector(self, attrs: Dict[str, str]) -> str:
        return "][".join([f"{key}='{value}'" for key, value in attrs.items()]) if attrs else ""


class Dropdown(Widget):
    """Represents a Dropdown element."""

    def __init__(self, controller: Any, **kwargs: str):
        selector = f"select[{self._build_selector(kwargs)}]"
        super().__init__(controller, selector)

    def _build_selector(self, attrs: Dict[str, str]) -> str:
        return "][".join([f"{key}='{value}'" for key, value in attrs.items()]) if attrs else ""

    def select_option(self, value: str, timeout: int = 10) -> None:
        """Selects an option from the dropdown."""
        dropdown = self.controller.page.locator(self.selector)
        dropdown.select_option(value)


class Icon(Widget):
    """Represents an Icon element (e.g., FontAwesome, Material Icons)."""

    def __init__(self, controller: Any, **kwargs: str):
        selector = f"i[{self._build_selector(kwargs)}], svg[{self._build_selector(kwargs)}]"
        super().__init__(controller, selector)

    def _build_selector(self, attrs: Dict[str, str]) -> str:
        return "][".join([f"{key}='{value}'" for key, value in attrs.items()]) if attrs else ""


class TextInput(Widget):
    """Represents a Text Input field."""

    def __init__(self, controller: Any, **kwargs: str):
        selector = f"input[type='text'][{self._build_selector(kwargs)}], input[type='password'][{self._build_selector(kwargs)}], input[type='email'][{self._build_selector(kwargs)}]"
        super().__init__(controller, selector)

    def _build_selector(self, attrs: Dict[str, str]) -> str:
        return "][".join([f"{key}='{value}'" for key, value in attrs.items()]) if attrs else ""

    def clear_and_type(self, text: str, timeout: int = 10) -> None:
        """Clears the field and enters new text."""
        input_field = self.controller.page.locator(self.selector)
        input_field.clear()
        input_field.fill(text)
