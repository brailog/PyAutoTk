import time
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session
from pyautotk.core.exceptions import ElementNotVisibleException


@browser_session(url="https://www.youtube.com/")
def watch_shorts(session, swipe_times=5):
    Widget(session, text="Shorts").click()
    en_button_down = Widget(session, aria_label="Next video")
    pt_button_down = Widget(session, aria_label="Proximo vídeo")
    for swipe in range(swipe_times):
        try:
            en_button_down.wait_for()
            en_button_down.click()
        except ElementNotVisibleException:
            pt_button_down.wait_for()
            pt_button_down.click()
        time.sleep(1)


@browser_session(url="https://www.google.com")
def search_google(session, search_input="PyAutoTk"):
    Widget(session, aria_label="Pesquisar").enter_text(search_input)
    Widget(session, aria_label="Pesquisa Google").click()
    time.sleep(1)


def main():
    print("Running Google Search example...")
    search_google()
    print("Running YouTube Shorts example...")
    watch_shorts()


if __name__ == "__main__":
    main()
