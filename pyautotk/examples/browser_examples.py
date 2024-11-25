import time
import pytest
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session
from pyautotk.core.config_loader import config


@pytest.fixture(scope="module")
def browser_setup():
    """
    Provides browser configuration for the tests.
    """
    config.browser_type = "firefox"
    config.log_level = "DEBUG"


@pytest.mark.parametrize("swipe_times", [5])
def test_watch_shorts(browser_setup, swipe_times):
    """
    Tests the functionality of watching YouTube Shorts.
    
    Args:
        browser_setup (dict): Browser configuration settings. (pytest fixture)
        swipe_times (int): Number of Shorts to swipe through.
    """
    @browser_session(url="https://www.youtube.com/")
    def watch_shorts(session) -> bool:
        Widget(session, text="Shorts").click()
        next_short_btn = Widget(session, aria_label="Próximo vídeo")
        for _ in range(swipe_times):
            next_short_btn.click()
            time.sleep(1)
        
        return True

    assert watch_shorts()


@pytest.mark.parametrize("search_input", ["Python"])
def test_search_google(browser_setup, search_input):
    """
    Tests the Google search functionality.

    Args:
        browser_setup (dict): Browser configuration settings. (pytest fixture)
        search_input (str): The search term to input in Google.
    """
    @browser_session(url="https://www.google.com")
    def search_google(session) -> bool:
        Widget(session, aria_label="Pesquisar").enter_text(search_input)
        Widget(session, aria_label="Pesquisa Google").click()
        time.sleep(3)
        return True

    assert search_google()


def test_navigate_via_reddit(browser_setup):
    """
    Tests navigation on Reddit to the r/Python community.

    Args:
        browser_setup (dict): Browser configuration settings. (pytest fixture)
    """
    @browser_session(url="https://www.reddit.com/")
    def navigate_via_reddit(session) -> bool:
        Widget(session, text="Tecnologia").click()
        Widget(session, text="Programação").click()

        return True
    assert navigate_via_reddit()
