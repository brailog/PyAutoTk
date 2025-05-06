import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

# Configuração do path
base_dir = os.path.dirname(os.path.abspath(__file__))
MOCKUP_TEST_URL_FILE = os.path.join(base_dir, "playground.html")

def setup_driver():
    driver = webdriver.Chrome()
    driver.get(f"file://{MOCKUP_TEST_URL_FILE}")
    return driver

def test_buttons():
    driver = setup_driver()
    
    try:
        # Clicar em botões
        primary_btn = driver.find_element(By.ID, "primary-btn")
        primary_btn.click()

        # Verificar mensagem
        message = driver.find_element(By.ID, "button-click-message").text
        assert "Botão Primário" in message

        # Clicar em botão secundário
        secondary_btn = driver.find_element(By.ID, "secondary-btn")
        secondary_btn.click()

        # Verificar se botão desativado está realmente desativado
        disabled_btn = driver.find_element(By.ID, "disabled-btn")
        assert not disabled_btn.is_enabled()
    finally:
        driver.quit()

def test_form():
    driver = setup_driver()
    
    try:
        # Preencher formulário
        driver.find_element(By.ID, "text-input").send_keys("Texto de teste")
        driver.find_element(By.ID, "email-input").send_keys("teste@exemplo.com")
        driver.find_element(By.ID, "password-input").send_keys("senha123")
        driver.find_element(By.ID, "number-input").send_keys("42")

        # Selecionar checkbox
        checkbox2 = driver.find_element(By.ID, "checkbox2")
        if checkbox2.is_selected():
            checkbox2.click()  # Desmarcar se já estiver marcado
        checkbox2.click()  # Marcar

        # Selecionar radio button
        driver.find_element(By.ID, "radio2").click()

        # Selecionar dropdown
        dropdown = Select(driver.find_element(By.ID, "dropdown"))
        dropdown.select_by_visible_text("Opção 2")

        # Submeter formulário
        driver.find_element(By.ID, "submit-btn").click()

        # Verificar resultado
        form_data = driver.find_element(By.ID, "form-data").text
        assert "teste@exemplo.com" in form_data
        assert "senha123" in form_data
    finally:
        driver.quit()

def test_hover():
    driver = setup_driver()
    
    try:
        hover_div = driver.find_element(By.ID, "hover-div")
        hover_status = driver.find_element(By.ID, "hover-status")

        # Verificar estado inicial
        assert "não está" in hover_status.text

        # Realizar hover
        actions = ActionChains(driver)
        actions.move_to_element(hover_div).perform()

        # Verificar estado após hover
        assert "está sobre" in hover_status.text
    finally:
        driver.quit()

def test_tabs():
    driver = setup_driver()
    
    try:
        # Verificar tab inicial
        tab1_content = driver.find_element(By.ID, "tab1")
        assert "primeira" in tab1_content.text

        driver.find_element(By.CSS_SELECTOR, "[data-tab='tab2']").click()

        tab2_content = driver.find_element(By.ID, "tab2")
        assert "segunda" in tab2_content.text
    finally:
        driver.quit()

def test_modal():
    driver = setup_driver()
    
    try:
        # Abrir modal
        driver.find_element(By.ID, "open-modal-btn").click()

        # Verificar se modal está visível
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "test-modal"))
        )
        assert modal.is_displayed()

        # Fechar modal
        driver.find_element(By.CLASS_NAME, "close").click()

        # Verificar se modal foi fechado
        assert not modal.is_displayed()
    finally:
        driver.quit()

def test_alerts_toasts():
    driver = setup_driver()
    
    try:
        # Mostrar alerta de sucesso
        driver.find_element(By.ID, "success-alert-btn").click()

        # Verificar alerta
        alert = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "Sucesso!" in alert.text

        # Mostrar toast
        driver.find_element(By.ID, "toast-btn").click()
        toast = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "toast")))
        assert "toast" in toast.text
    finally:
        driver.quit()

def test_drag_and_drop():
    driver = setup_driver()
    
    try:
        source = driver.find_element(By.ID, "drag-source")
        target = driver.find_element(By.ID, "drop-target")
        status = driver.find_element(By.ID, "dragdrop-status")

        # Simular drag and drop
        actions = ActionChains(driver)
        actions.click_and_hold(source).move_to_element(target).release().perform()

        # Verificar status
        assert "solto" in status.text
    finally:
        driver.quit()

if __name__ == "__main__":
    test_buttons()
    #test_links()
    test_form()
    test_hover()
    test_tabs()
    test_modal()
    test_alerts_toasts()
    test_drag_and_drop()
    print("Todos os testes foram executados com sucesso!")