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
