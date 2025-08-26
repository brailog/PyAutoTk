import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

base_dir = os.path.dirname(os.path.abspath(__file__))
MOCKUP_TEST_URL_FILE = "http://localhost:8080/"


def start(driver):
    xpath = "//*[@id='start-btn' and contains(text(), 'Começar')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def test_botoes(driver):
    xpath_primary = "//*[@id='primary-btn' and contains(text(), 'Botão Primário')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_primary))).click()
    message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "button-click-message")))
    assert "Botão Primário" in message_element.text

    xpath_secondary = "//*[@id='secondary-btn' and contains(text(), 'Botão Secundário')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_secondary))).click()
    message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "button-click-message")))
    assert "Botão Secundário" in message_element.text

    xpath_danger = "//*[@id='danger-btn' and contains(text(), 'Botão Perigo')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_danger))).click()
    message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "button-click-message")))
    assert "Botão Perigo" in message_element.text
    
    disabled_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "disabled-btn")))
    assert not disabled_btn.is_enabled()

    xpath_next = "//*[contains(text(), 'Próximo')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_next))).click()


def test_links(driver):
    original_window = driver.current_window_handle
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "simple-link"))).click()
    WebDriverWait(driver, 5).until(EC.alert_is_present()).accept()

    xpath_new_tab = "//*[@id='new-tab-link' and contains(text(), 'Link em Nova Aba')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_new_tab))).click()
    WebDriverWait(driver, 5).until(EC.alert_is_present()).accept()

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    new_tab_handle = [handle for handle in driver.window_handles if handle != original_window][0]
    driver.switch_to.window(new_tab_handle)

    driver.close()
    driver.switch_to.window(original_window)

    xpath_download = "//*[@id='download-link' and contains(text(), 'Link de Download')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_download))).click()
    time.sleep(0.5)

    xpath_next = "//*[contains(text(), 'Próximo')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_next))).click()


def test_formularios(driver):
    dummy_file_path = os.path.abspath(os.path.join(base_dir, "dummy_upload.txt"))
    with open(dummy_file_path, "w") as f:
        f.write("This is a dummy text file to test file upload.")

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "text-input"))).send_keys("Texto de teste")
        driver.find_element(By.ID, "email-input").send_keys("teste@exemplo.com")
        driver.find_element(By.ID, "password-input").send_keys("senha123")
        driver.find_element(By.ID, "number-input").send_keys(str(random.randint(1, 100)))
        driver.find_element(By.ID, "date-input").send_keys("11121999")

        color_input = driver.find_element(By.ID, "color-input")
        new_color = "#EEFF00"
        driver.execute_script("arguments[0].value = arguments[1];", color_input, new_color)
        retrieved_color = color_input.get_attribute("value")
        assert retrieved_color.lower() == new_color.lower()
        
        file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "file-input")))
        file_input.send_keys(dummy_file_path)
        
        range_input = driver.find_element(By.ID, "range-input")
        new_range_value = str(random.randint(1, 100))
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));", range_input, new_range_value)
        assert range_input.get_attribute("value") == new_range_value

        driver.find_element(By.ID, "textarea-input").send_keys(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus eget nisi quam."
        )
        driver.find_element(By.XPATH, "//*[@type='checkbox' and @value='opcao2']").click()
        driver.find_element(By.XPATH, "//*[@type='checkbox' and @value='opcao1']").click()
        driver.find_element(By.XPATH, "//*[@type='radio' and @value='opcao2']").click()
        
        single_dropdown_el = driver.find_element(By.ID, "dropdown")
        ActionChains(driver).scroll_to_element(single_dropdown_el).perform()
        single_select = Select(single_dropdown_el)
        single_select.select_by_visible_text("Opção 2")
        assert [opt.text for opt in single_select.all_selected_options] == ["Opção 2"]

        multi_dropdown_el = driver.find_element(By.ID, "multi-dropdown")
        multi_select = Select(multi_dropdown_el)
        multi_select.select_by_visible_text("Opção 1")
        multi_select.select_by_index(2)
        assert sorted([opt.text for opt in multi_select.all_selected_options]) == ["Opção 1", "Opção 3"]
        multi_select.deselect_by_visible_text("Opção 1")
        assert [opt.text for opt in multi_select.all_selected_options] == ["Opção 3"]

        driver.find_element(By.ID, "submit-btn").click()

        form_data = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "form-data"))).text
        assert "dummy_upload.txt" in form_data
    finally:
        if os.path.exists(dummy_file_path):
            os.remove(dummy_file_path)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Próximo')]"))).click()


def test_hover(driver):
    hover_div = driver.find_element(By.ID, "hover-div")
    hover_status = driver.find_element(By.ID, "hover-status")
    body = driver.find_element(By.TAG_NAME, "body")

    assert "não está" in hover_status.text
    for _ in range(3):
        ActionChains(driver).move_to_element(hover_div).perform()
        assert "está sobre" in hover_status.text
        time.sleep(0.5)
        
        ActionChains(driver).move_to_element(body).perform()
        assert "não está" in hover_status.text

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Próximo')]"))).click()


def test_tabs(driver):
    tab1_content = driver.find_element(By.ID, "tab1")
    assert "primeira" in tab1_content.text
    
    driver.find_element(By.XPATH, "//*[@data-tab='tab2']").click()
    tab2_content = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "tab2")))
    assert "segunda" in tab2_content.text

    driver.find_element(By.XPATH, "//*[@data-tab='tab3']").click()
    tab3_content = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "tab3")))
    assert "terceira" in tab3_content.text

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Próximo')]"))).click()


def test_modal(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "open-modal-btn"))).click()
    
    modal_xpath = "//*[@class='modal' and @id='test-modal']"
    modal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, modal_xpath)))

    assert "modal simples que pode ser" in modal.text
    assert modal.is_displayed()

    close_btn = driver.find_element(By.CLASS_NAME, "close")
    assert close_btn.is_displayed()
    close_btn.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Próximo')]"))).click()


def test_alertas(driver):
    driver.find_element(By.ID, "success-alert-btn").click()
    
    alert_success = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success")))
    assert "Sucesso!" in alert_success.text

    driver.find_element(By.ID, "warning-alert-btn").click()
    alert_warning = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-warning")))
    assert "Aviso!" in alert_warning.text

    driver.find_element(By.ID, "info-alert-btn").click()
    alert_info = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-info")))
    assert "Informação!" in alert_info.text

    driver.find_element(By.ID, "error-alert-btn").click()
    alert_error = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
    assert "Erro!" in alert_error.text

    driver.find_element(By.ID, "toast-btn").click()
    
    toast_xpath = "//*[@id='toast' and @class='toast show-toast']"
    toast = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, toast_xpath)))
    assert "toast!" in toast.text

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Próximo')]"))).click()


def test_drag_and_drop(driver):
    
    source_drag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "drag-source")))
    target_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "drop-target")))
    status = driver.find_element(By.ID, "dragdrop-status")

    assert "Nenhuma" in status.text
    ActionChains(driver).drag_and_drop(source_drag, target_drop).perform()
    assert "solto" in status.text


def full_execution():
    """
    Sets up the Selenium driver, runs all tests, and tears down the driver.
    This replaces the `@browser_session` decorator from PyAutoTk.
    """
    # Using Firefox, but you can easily swap to Chrome
    driver = webdriver.Chrome()
    #driver = webdriver.Firefox()
    try:
        driver.maximize_window()
        driver.get(MOCKUP_TEST_URL_FILE)
        start(driver)
        test_botoes(driver)
        test_links(driver)
        test_formularios(driver)
        test_hover(driver)
        test_tabs(driver)
        test_modal(driver)
        test_alertas(driver)
        test_drag_and_drop(driver)

    finally:
        print("Closing browser session.")
        driver.quit()


if __name__ == "__main__":
    full_execution()
    print("Todos os testes do Selenium foram executados com sucesso!")
