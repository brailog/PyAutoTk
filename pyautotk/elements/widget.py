import re
from typing import Dict, Any
from pyautotk.core.logger_utils import initialize_logger


class Widget:
    """
    Represents a UI element on the page and provides methods to interact with it using the specified controller.
    """

    def __init__(self, controller: Any, **kwargs: str) -> None:
        """
        Initializes the Widget with the specified controller and attributes for XPath construction.

        Args:
            controller (Any): The controller instance to use for interacting with the element (e.g., BrowserController).
            **kwargs (str): Keyword arguments representing the attributes of the element to build the XPath.
        """
        self.logger = initialize_logger(self.__class__.__name__)
        self.logger.debug(f"Initializing Widget with attributes: {kwargs}")

        self.controller = controller
        self.attrs = kwargs
        self.xpath = self._build_xpath()

        self.logger.info(f"Constructed XPath for Widget: {self.xpath}")

    def click(self, timeout: int = 10) -> None:
        """
        Clicks on the element identified by the constructed XPath.

        Args:
            timeout (int): Maximum time to wait for the element to be present before clicking. Default is 10 seconds.
        """
        self.logger.info(
            f"Attempting to click on element with XPath: {self.xpath} (Timeout: {timeout} seconds)"
        )
        try:
            self.controller.click_element(self.xpath, timeout)
        except Exception as e:
            self.logger.error(f"Failed to click on element with XPath: {self.xpath}. Error: {e}")
            raise

    def enter_text(self, text: str, timeout: int = 10) -> None:
        """
        Enters text into the element (e.g., an input field) identified by the XPath.

        Args:
            text (str): The text to be entered into the element.
            timeout (int): Maximum time to wait for the element to be present before entering text. Default is 10 seconds.
        """
        self.logger.info(f"Entering text '{text}' into element with XPath: {self.xpath}")
        self.click()  # Ensure the element is focused before entering text
        try:
            self.controller.enter_text(self.xpath, text, timeout)
        except Exception as e:
            self.logger.error(
                f"Failed to enter text into element with XPath: {self.xpath}. Error: {e}"
            )
            raise

    def scroll_to(self, timeout: int = 10) -> None:
        """
        Scrolls to the element using the specified XPath.

        Args:
            timeout (int): Maximum time to wait for the element to be present before scrolling. Default is 10 seconds.
        """
        self.logger.info(
            f"Scrolling to element with XPath: {self.xpath} (Timeout: {timeout} seconds)"
        )
        try:
            self.controller.scroll_to_element(self.xpath, timeout)
        except Exception as e:
            self.logger.error(f"Failed to scroll to element with XPath: {self.xpath}. Error: {e}")
            raise

    def wait_for(self, timeout: int = 10) -> Any:
        """
        Waits until the element identified by the XPath is visible.

        Args:
            timeout (int): Maximum time to wait for the element to become visible. Default is 10 seconds.

        Returns:
            Any: The WebElement if found and visible, or raises an exception if not found.
        """
        self.logger.info(
            f"Waiting for element with XPath: {self.xpath} to become visible (Timeout: {timeout} seconds)"
        )
        try:
            element = self.controller.wait_for_element(self.xpath, timeout)
            self.logger.info(f"Element with XPath: {self.xpath} is now visible.")
            return element
        except Exception as e:
            self.logger.error(f"Failed to wait for element with XPath: {self.xpath}. Error: {e}")
            raise

    @staticmethod
    def get_all_elements_with_attribute(controller: Any, attribute: str) -> Dict[str, str]:
        """
        Retrieves all elements in the page that have a specific attribute.

        Args:
            controller (Any): The controller instance to use for locating the elements.
            attribute (str): The attribute to search for in the elements.

        Returns:
            Dict[str, WebElement]: A dictionary where the keys are the attribute values and the values are the corresponding WebElements.
        """
        logger = initialize_logger("Widget")
        logger.info(f"Retrieving all elements with attribute: {attribute}")
        try:
            elements = controller.find_elements(f"//*[@{attribute}]")
            return elements
        except Exception as e:
            logger.error(f"Failed to retrieve elements with attribute: {attribute}. Error: {e}")
            raise

    def _build_xpath(self) -> str:
        """
        Constructs the XPath string based on the provided attributes.

        Returns:
            str: The constructed XPath for locating the element.
        """
        xpath = "//*"
        conditions = []
        for attr, value in self.attrs.items():
            attr = re.sub(r"_", "-", attr)
            if attr == "text":
                conditions.append(f"contains(text(), '{value}')")
            elif "class-" in attr:
                conditions.append(f"@class='{value}'")
            else:
                conditions.append(f"@{attr}='{value}'")

        if conditions:
            xpath += "[" + " and ".join(conditions) + "]"
        self.logger.debug(f"Generated XPath: {xpath} based on attributes: {self.attrs}")
        return xpath
