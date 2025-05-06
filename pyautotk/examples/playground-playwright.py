import os
from playwright.sync_api import sync_playwright

# Configuração do path
base_dir = os.path.dirname(os.path.abspath(__file__))
MOCKUP_TEST_URL_FILE = os.path.join(base_dir, "playground.html")

def setup_page():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{MOCKUP_TEST_URL_FILE}")
    return playwright, browser, page

def teardown(playwright, browser):
    browser.close()
    playwright.stop()

def test_buttons():
    playwright, browser, page = setup_page()
    
    try:
        page.click("#primary-btn")
        message = page.text_content("#button-click-message")
        assert "Botão Primário" in message
        
        page.click("#secondary-btn")
        is_disabled = page.is_disabled("#disabled-btn")
        assert is_disabled
    finally:
        teardown(playwright, browser)

def test_form():
    playwright, browser, page = setup_page()
    
    try:
        page.fill("#text-input", "Texto de teste")
        page.fill("#email-input", "teste@exemplo.com")
        page.fill("#password-input", "senha123")
        page.fill("#number-input", "42")
        page.click("#radio2")
        page.click("#Opção 2")
        page.click("#submit-btn")
        
        form_data = page.text_content("#form-data")
        assert "teste@exemplo.com" in form_data
        assert "senha123" in form_data
    finally:
        teardown(playwright, browser)

def test_hover():
    playwright, browser, page = setup_page()
    
    try:
        status = page.text_content("#hover-status")
        assert "não está" in status
        page.hover("#hover-div")
        status = page.text_content("#hover-status")
        assert "está sobre" in status
    finally:
        teardown(playwright, browser)

def test_tabs():
    playwright, browser, page = setup_page()
    
    try:
        tab1 = page.locator("#tab1")
        assert "active" in tab1.get_attribute("class")
        page.click("[data-tab='tab2']")
        tab2 = page.locator("#tab2")
        assert "active" in tab2.get_attribute("class")
        assert "segunda tab" in tab2.text_content()
    finally:
        teardown(playwright, browser)

def test_modal():
    playwright, browser, page = setup_page()
    
    try:
        page.click("#open-modal-btn")
        modal = page.locator("#test-modal")
        assert modal.is_visible()
        page.click(".close")
        assert modal.is_hidden()
    finally:
        teardown(playwright, browser)

def test_alerts_toasts():
    playwright, browser, page = setup_page()
    
    try:
        page.click("#success-alert-btn")
        alert = page.locator(".alert-success")
        assert alert.is_visible()
        assert "Sucesso!" in alert.text_content()
        page.click("#toast-btn")
        toast = page.locator("#toast")
        assert toast.is_visible()
        assert "toast" in toast.text_content()
    finally:
        teardown(playwright, browser)

if __name__ == "__main__":
    test_buttons()
    #test_links()
    test_form()
    test_hover()
    test_tabs()
    test_modal()
    test_alerts_toasts()
    print("Todos os testes do Playwright foram executados com sucesso!")