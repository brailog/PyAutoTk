class ElementNotVisibleException(Exception):
    """
    Custom exception raised when an element is not visible within the specified timeout.
    """

    def __init__(self, xpath: str, timeout: int, original_exception: Exception):
        self.xpath = xpath
        self.timeout = timeout
        self.original_exception = original_exception
        super().__init__(
            f"Element with XPath '{xpath}' not visible after {timeout} seconds. Error: {original_exception}"
        )

class WidgetException(Exception):
    """
    Base exception for errors related to Widget operations.
    """
    def __init__(self, message: str):
        super().__init__(message)


class WidgetClickException(WidgetException):
    """
    Exception raised when a click operation fails on the Widget.
    """
    def __init__(self, xpath: str, original_exception: Exception):
        message = f"Failed to click on element with XPath '{xpath}'. Error: {original_exception}"
        super().__init__(message)


class WidgetDoubleClickException(WidgetException):
    """
    Exception raised when a double-click operation fails on the Widget.
    """
    def __init__(self, xpath: str, original_exception: Exception):
        message = f"Failed to double-click on element with XPath '{xpath}'. Error: {original_exception}"
        super().__init__(message)


class WidgetHoverException(WidgetException):
    """
    Exception raised when a hover action fails on the Widget.
    """
    def __init__(self, xpath: str, original_exception: Exception):
        message = f"Failed to hover over element with XPath '{xpath}'. Error: {original_exception}"
        super().__init__(message)


class WidgetEnterTextException(WidgetException):
    """
    Exception raised when entering text into a Widget element fails.
    """
    def __init__(self, xpath: str, text: str, original_exception: Exception):
        message = f"Failed to enter text '{text}' into element with XPath '{xpath}'. Error: {original_exception}"
        super().__init__(message)


class WidgetScrollException(WidgetException):
    """
    Exception raised when scrolling to a Widget element fails.
    """
    def __init__(self, xpath: str, original_exception: Exception):
        message = f"Failed to scroll to element with XPath '{xpath}'. Error: {original_exception}"
        super().__init__(message)


class WidgetWaitTimeoutException(WidgetException):
    """
    Exception raised when a Widget element is not found or becomes visible within the specified timeout.
    """
    def __init__(self, xpath: str, timeout: int, original_exception: Exception):
        message = f"Element with XPath '{xpath}' not visible after {timeout} seconds. Error: {original_exception}"
        super().__init__(message)


class WidgetRetrievePropertiesException(WidgetException):
    """
    Exception raised when retrieving properties of a Widget element fails.
    """
    def __init__(self, xpath: str, original_exception: Exception):
        message = f"Failed to retrieve properties for element with XPath '{xpath}'. Error: {original_exception}"
        super().__init__(message)


class WidgetAttributeException(WidgetException):
    """
    Exception raised when retrieving an attribute from a Widget element fails.
    """
    def __init__(self, xpath: str, attribute_name: str, original_exception: Exception):
        message = f"Failed to retrieve attribute '{attribute_name}' from element with XPath '{xpath}'. Error: {original_exception}"
        super().__init__(message)


class WidgetExtractionException(WidgetException):
    """
    Exception raised when extracting elements or attributes from the Widget fails.
    """
    def __init__(self, attribute: str, original_exception: Exception):
        message = f"Failed to extract elements with attribute '{attribute}'. Error: {original_exception}"
        super().__init__(message)


class BrowserWaitForPageLoadException(WidgetException):
    """
    Exception raised when the page does not load within the specified timeout.
    """
    def __init__(self, timeout: int):
        message = f"Page did not load completely within {timeout} seconds."
        super().__init__(message)
