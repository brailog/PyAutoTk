from functools import wraps
from controllers.browser.browser_controller import BrowserController


def browser_session(url: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = BrowserController()
            try:
                session.open_url(url)
                return func(session, *args, **kwargs)
            finally:
                session.kill_browser()
        return wrapper
    return decorator
