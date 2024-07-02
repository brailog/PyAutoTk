from controllers.browser.pages.linkedin import Linkedin
from controllers.browser.pages.google import Google
from controllers.browser.browser_controller import BrowserController


class BrowserConnection:
    def __init__(self):
        self._browser_controller = BrowserController()
        self.driver = self._browser_controller.driver

    @property
    def linkedin(self) -> 'Linkedin':
        self._linkedin = Linkedin(self.driver)
        return self._linkedin

    @property
    def google(self) -> 'Google':
        self._google = Google(self.driver)
        return self._google

    def end(self) -> None:
        self._browser_controller.end()
