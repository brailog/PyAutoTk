import re
import time
from typing import Dict, Any, List
from pyautotk.core.logger_utils import initialize_logger
from pyautotk.core.exceptions import WidgetWaitTimeoutException
from pyautotk.core.exceptions import WidgetClickException
from pyautotk.core.exceptions import WidgetDoubleClickException
from pyautotk.core.exceptions import WidgetHoverException
from pyautotk.core.exceptions import WidgetEnterTextException
from pyautotk.core.exceptions import WidgetScrollException
from pyautotk.core.exceptions import WidgetRetrievePropertiesException
from pyautotk.core.exceptions import WidgetAttributeException
from pyautotk.core.exceptions import WidgetExtractionException

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

        self.logger.debug(f"Constructed XPath for Widget: {self.xpath}")

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
            self.controller._click_element(self.xpath, timeout)
        except Exception as e:
            self.logger.error(f"Failed to click on element with XPath: {self.xpath}. Error: {e}")
            raise WidgetClickException(self.xpath, e)

    def double_click(self, delay: float = 0.1, timeout: int = 10) -> None:
        """
        Performs a double-click on the element.

        Args:
            timeout (int): Maximum time to wait for the element. Default is 10 seconds.
        """
        self.logger.info(f"Performing double-click on element with XPath: {self.xpath}")
        try:
            for _ in range(2):
                self.click(timeout)
                time.sleep(delay)
        except Exception as e:
            self.logger.error(f"Failed to double-click on element. Error: {e}")
            raise WidgetDoubleClickException(self.xpath, e)

    def hover(self, timeout: int = 10) -> None:
        """
        Simulates a mouse hover action over the element identified by the XPath.

        Args:
            timeout (int): Maximum time to wait for the element to become present before hovering. Default is 10 seconds.

        Raises:
            Exception: If the element cannot be found or the hover action fails.
        """
        self.logger.info(f"Attempting to hover over element with XPath: {self.xpath} (Timeout: {timeout} seconds)")
        try:
            self.controller._hover_element(self.x)
            self.logger.info(f"Successfully hovered over element with XPath: {self.xpath}")
        except Exception as e:
            self.logger.error(f"Failed to hover over element with XPath: {self.xpath}. Error: {e}")
            raise WidgetHoverException(self.xpath, e)

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
            self.controller._enter_text_safely(self.xpath, text, timeout)
        except Exception as e:
            self.logger.error(
                f"Failed to enter text into element with XPath: {self.xpath}. Error: {e}"
            )
            raise WidgetEnterTextException(self.xpath, e)

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
            self.controller._scroll_to_element(self.xpath, timeout)
        except Exception as e:
            self.logger.error(f"Failed to scroll to element with XPath: {self.xpath}. Error: {e}")
            raise WidgetScrollException(self.xpath, e)

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
            element = self.controller._wait_for_element(self.xpath, timeout)
            self.logger.info(f"Element with XPath: {self.xpath} is now visible.")
            return element
        except Exception as e:
            self.logger.error(f"Failed to wait for element with XPath: {self.xpath}. Error: {e}")
            raise WidgetWaitTimeoutException(self.xpath, timeout, e)


    def get_element_properties(self, timeout: int = 10) -> Dict[str, Any]:
        """
        Extracts and returns properties of the first element identified by the XPath.

        Args:
            timeout (int): Maximum time to wait for the element to be present before retrieving properties. Default is 10 seconds.

        Returns:
            Dict[str, Any]: A dictionary containing properties for the first matching element.

        Raises:
            Exception: If the properties cannot be retrieved.
        """
        self.logger.info(f"Attempting to retrieve information from the first element with XPath: {self.xpath} (Timeout: {timeout} seconds)")
        try:
            element = self.controller._wait_for_element(self.xpath, timeout)
            element_data = self._extract_element_properties(element)

            self.logger.info(f"Successfully retrieved information for the element: {element_data}")
            return element_data
        except Exception as e:
            self.logger.error(f"Failed to retrieve information from element with XPath: {self.xpath}. Error: {e}")
            raise WidgetRetrievePropertiesException(self.xpath, e)


    def get_all_elements_properties(self, timeout: int = 10) -> List[Dict[str, Any]]:
        """
        Extracts and returns properties of all elements that match the XPath.

        Args:
            timeout (int): Maximum time to wait for the elements to be present before retrieving properties. Default is 10 seconds.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing properties for a matching element.

        Raises:
            Exception: If the properties cannot be retrieved.
        """
        self.logger.info(f"Attempting to retrieve information from all elements with XPath: {self.xpath} (Timeout: {timeout} seconds)")
        try:
            elements = self.controller._wait_for_all_elements(self.xpath)
            elements_data = [self._extract_element_properties(element) for element in elements]

            self.logger.info(f"Successfully retrieved information for {len(elements_data)} elements.")
            return elements_data
        except Exception as e:
            self.logger.error(f"Failed to retrieve information from elements with XPath: {self.xpath}. Error: {e}")
            raise WidgetRetrievePropertiesException(self.xpath, e)


    def get_attribute(self, attribute_name: str, timeout: int = 10) -> str:
        """
        Retrieves the value of a specific attribute from the element.

        Args:
            attribute_name (str): The name of the attribute to retrieve.
            timeout (int): Maximum time to wait for the element. Default is 10 seconds.

        Returns:
            str: The value of the specified attribute, or None if not found.
        """
        self.logger.info(f"Getting attribute '{attribute_name}' for element with XPath: {self.xpath}")
        try:
            element = self.controller._wait_for_element(self.xpath, timeout)
            return element.get_attribute(attribute_name)
        except Exception as e:
            self.logger.error(f"Failed to get attribute '{attribute_name}'. Error: {e}")
            raise WidgetAttributeException(self.xpath, e)

    @staticmethod
    def extract_all_elements_with_attribute(controller: Any, attribute: str) -> Dict[str, str]:
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
            elements = controller._wait_for_element(f"//*[@{attribute}]")
            return elements
        except Exception as e:
            logger.error(f"Failed to retrieve elements with attribute: {attribute}. Error: {e}")
            raise WidgetExtractionException(attribute, e)

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

    def _extract_element_properties(self, element: Any) -> Dict[str, Any]:
        """
        Extracts properties from a single element.

        Args:
            element (Any): The WebElement to extract properties from.

        Returns:
            Dict[str, Any]: A dictionary containing properties for the given element.
        """
        attributes = {
            attr_name: element.get_attribute(attr_name)
            for attr_name in ["id", "class", "name", "type", "value", "href", "src", "alt", "aria-label"]
            if element.get_attribute(attr_name) is not None
        }

        return {
            "text": element.text,
            "tag_name": element.tag_name,
            "attributes": attributes,
            "location": element.location,
            "size": element.size,
            "is_displayed": element.is_displayed(),
            "is_enabled": element.is_enabled(),
        }
