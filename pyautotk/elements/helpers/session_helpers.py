from functools import wraps
from pyautotk.core.browser_controller import BrowserController


def browser_session(
    url: str,
    browser_type: str = "firefox",
    maximize: bool = False,
    headless: bool = False,
):
    """
    A decorator that manages a browser session using the BrowserController, with support for configuring
    the browser type, window size, and headless mode.

    This decorator automates the setup and teardown of the browser session. It initializes the
    BrowserController with the specified configuration, opens the URL, and closes the browser when the
    function completes. This simplifies the workflow by handling browser instantiation and cleanup.

    Args:
        url (str): The URL to open when starting the browser session.
        browser_type (str): The type of browser to use. Supported values are 'firefox' or 'chrome'. Default is 'firefox'.
        maximize (bool): Whether to start the browser maximized. Default is False.
        headless (bool): Whether to run the browser in headless mode. Default is False.

    Returns:
        Callable: The wrapped function with the browser session management.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper function that initializes the BrowserController with the given configuration,
            opens the URL, executes the decorated function, and ensures the browser is closed.

            Args:
                *args: Positional arguments to pass to the decorated function.
                **kwargs: Keyword arguments to pass to the decorated function.

            Returns:
                Any: The result of the decorated function.
            """
            session = BrowserController(
                browser_type=browser_type, maximize=maximize, headless=headless
            )
            try:
                session.open_url(url)
                return func(session, *args, **kwargs)
            finally:
                session.kill_browser()

        return wrapper

    return decorator
