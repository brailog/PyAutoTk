from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

class KeyboardController:
    def __init__(self, session_driver: WebDriver) -> None:
        """
        Initializes the Keyboard helper with an active WebDriver session.
        
        Args:
            session_driver (WebDriver): The active WebDriver instance.
        """
        self._actions = ActionChains(session_driver)

    def send_keys(self, key: str) -> None:
        """
        Sends a single key press to the current active element or browser context.
        
        Args:
            key (str): The key to be pressed.
        """
        self._actions.send_keys(key).perform()

    def press_enter(self) -> None:
        """Simulates pressing the Enter key."""
        self.send_keys(Keys.ENTER)

    def press_escape(self) -> None:
        """Simulates pressing the Escape key."""
        self.send_keys(Keys.ESCAPE)

    def press_tab(self) -> None:
        """Simulates pressing the Tab key."""
        self.send_keys(Keys.TAB)

    def press_arrow_up(self) -> None:
        """Simulates pressing the Up Arrow key."""
        self.send_keys(Keys.ARROW_UP)

    def press_arrow_down(self) -> None:
        """Simulates pressing the Down Arrow key."""
        self.send_keys(Keys.ARROW_DOWN)

    def press_arrow_left(self) -> None:
        """Simulates pressing the Left Arrow key."""
        self.send_keys(Keys.ARROW_LEFT)

    def press_arrow_right(self) -> None:
        """Simulates pressing the Right Arrow key."""
        self.send_keys(Keys.ARROW_RIGHT)

    def press_backspace(self) -> None:
        """Simulates pressing the Backspace key."""
        self.send_keys(Keys.BACKSPACE)

    def press_delete(self) -> None:
        """Simulates pressing the Delete key."""
        self.send_keys(Keys.DELETE)

    def press_space(self) -> None:
        """Simulates pressing the Spacebar."""
        self.send_keys(Keys.SPACE)

    def press_control(self) -> None:
        """Simulates pressing the Control key."""
        self.send_keys(Keys.CONTROL)

    def press_shift(self) -> None:
        """Simulates pressing the Shift key."""
        self.send_keys(Keys.SHIFT)

    def press_alt(self) -> None:
        """Simulates pressing the Alt key."""
        self.send_keys(Keys.ALT)

    def press_function_key(self, function_key: int) -> None:
        """
        Simulates pressing a function key (F1 through F12).
        
        Args:
            function_key (int): The number of the function key (1-12).
        """
        if 1 <= function_key <= 12:
            self.send_keys(getattr(Keys, f"F{function_key}"))
        else:
            raise ValueError("Function key must be between 1 and 12.")


class MouseController:
    def __init__(self):
        pass