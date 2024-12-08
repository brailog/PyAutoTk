import time
import pytest
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session
from pyautotk.elements.helpers.input_helpers import Keyboard
from pyautotk.core.config_loader import config
from pyautotk.core.exceptions import WidgetClickException

SWIPE = 10

@browser_session("https://www.tiktok.com/")
def watch_tiktok(session):
    generical_swipe_for_small_videos_interface(session, "Para você")

@browser_session(url="https://www.youtube.com/")
def watch_shorts(session) -> bool:
    generical_swipe_for_small_videos_interface(session, "Shorts")

def generical_swipe_for_small_videos_interface(session, menu_option: str):
    keyboard = Keyboard(session)
    Widget(session, text=menu_option).click()
    skip_btn = Widget(session, text="Continuar como convidado")

    session.wait_for_initial_load()
    for _ in range(SWIPE):
        keyboard.arrow_down()
        skip_btn.click(timeout=1)

if __name__ == "__main__":
    watch_tiktok()
    #watch_shorts()