import time


from toolkits.browser.widget import Widget
from toolkits.utils.session_helpers import browser_session

@browser_session(url="https://www.youtube.com/")
def watch_shorts(session, swipe_times=10):
    Widget(session, text="Shorts").click()
    button_down = Widget(session, id="navigation-button-down")

    for swipe in range(swipe_times):
        button_down.wait_for()
        button_down.click()
        time.sleep(1)


@browser_session(url="https://www.google.com")
def search_google(session, search_input="PyAutoTk"):
    Widget(session, aria_label="Pesquisar").enter_text(search_input)
    Widget(session, aria_label="Pesquisa Google").click()
    time.sleep(5)
