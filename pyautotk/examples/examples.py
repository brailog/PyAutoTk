import time
import pytest
from pyautotk.elements.widget import Widget, SearchBar
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

@browser_session("https://www.reddit.com/")
def testssss(session):
    search_field = SearchBar(session, name="q", placeholder="Buscar no Reddit")
    search_field.click()  # Garante que o campo está focado
    search_field.enter_text("Automação com PyAutoTk")  # Digita um termo de busca
    search_field.press_enter()  # Pressiona Enter para buscar

def generical_swipe_for_small_videos_interface(session, menu_option: str):
    keyboard = Keyboard(session)
    Widget(session, text=menu_option).click()
    skip_btn = Widget(session, text="Continuar como convidado")

    session.wait_for_initial_load()
    for _ in range(SWIPE):
        keyboard.arrow_down()
        time.sleep(0.5)

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Abrir em modo visível para depuração
        page = browser.new_page()

        # Acessa a página do Reddit
        page.goto("https://www.reddit.com")

        # Espera até que o widget de busca esteja disponível
        page.wait_for_selector("reddit-search-large")

        # Seleciona o campo de entrada da barra de busca e insere um termo de pesquisa
        search_input = page.locator("reddit-search-large form input[name='q']").nth(0)
        search_input.fill("Playwright")
        
        # Pressiona Enter para buscar
        search_input.press("Enter")

        # Mantém o navegador aberto para visualização
        page.wait_for_timeout(5000)

        browser.close()
    
    sync_playwright()