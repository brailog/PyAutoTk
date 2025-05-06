from pyautotk.core.input import KeyboardController
from pyautotk.core.logger_utils import initialize_logger
from typing import Any


class Keyboard:
    def __init__(self, controller: Any) -> None:
        """
        Initializes the interface for keyboard actions.
        
        Args:
            controller (Any): The controller instance that provides keyboard actions.
        """
        self.logger = initialize_logger(self.__class__.__name__)
        self.controller = KeyboardController(controller.driver)

    def enter(self) -> None:
        """Simulates pressing the Enter key."""
        self.logger.info("Pressing Enter key.")
        self.controller.press_enter()

    def escape(self) -> None:
        """Simulates pressing the Escape key."""
        self.logger.info("Pressing Escape key.")
        self.controller.press_escape()

    def tab(self) -> None:
        """Simulates pressing the Tab key."""
        self.logger.info("Pressing Tab key.")
        self.controller.press_tab()

    def arrow_up(self) -> None:
        """Simulates pressing the Up Arrow key."""
        self.logger.info("Pressing Up Arrow key.")
        self.controller.press_arrow_up()

    def arrow_down(self) -> None:
        """Simulates pressing the Down Arrow key."""
        self.logger.info("Pressing Down Arrow key.")
        self.controller.press_arrow_down()

    def arrow_left(self) -> None:
        """Simulates pressing the Left Arrow key."""
        self.logger.info("Pressing Left Arrow key.")
        self.controller.press_arrow_left()

    def arrow_right(self) -> None:
        """Simulates pressing the Right Arrow key."""
        self.logger.info("Pressing Right Arrow key.")
        self.controller.press_arrow_right()

    def backspace(self) -> None:
        """Simulates pressing the Backspace key."""
        self.logger.info("Pressing Backspace key.")
        self.controller.press_backspace()

    def delete(self) -> None:
        """Simulates pressing the Delete key."""
        self.logger.info("Pressing Delete key.")
        self.controller.press_delete()

    def space(self) -> None:
        """Simulates pressing the Spacebar."""
        self.logger.info("Pressing Spacebar key.")
        self.controller.press_space()

    def control(self) -> None:
        """Simulates pressing the Control key."""
        self.logger.info("Pressing Control key.")
        self.controller.press_control()

    def shift(self) -> None:
        """Simulates pressing the Shift key."""
        self.logger.info("Pressing Shift key.")
        self.controller.press_shift()

    def alt(self) -> None:
        """Simulates pressing the Alt key."""
        self.logger.info("Pressing Alt key.")
        self.controller.press_alt()

    def function_key(self, function_key: int) -> None:
        """
        Simulates pressing a function key (F1 through F12).
        
        Args:
            function_key (int): The number of the function key (1-12).
        """
        if 1 <= function_key <= 12:
            self.logger.info(f"Pressing Function key F{function_key}.")
            self.controller.press_function_key(function_key)
        else:
            self.logger.error(f"Invalid Function key: F{function_key}. Must be between F1 and F12.")
            raise ValueError("Function key must be between F1 and F12.")