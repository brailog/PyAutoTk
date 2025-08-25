import time
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session
import os
from pyautotk.core.config_loader import config
import random
from pyautotk.elements.helpers.input_helpers import Keyboard

config.log_level = "DEBUG"

base_dir = os.path.dirname(os.path.abspath(__file__))
MOCKUP_TEST_URL_FILE = "http://localhost:8080/" # os.path.join(base_dir, "playground.html")

#@browser_session(MOCKUP_TEST_URL_FILE)
def start(session):
    botao_comecar = Widget(session, id="start-btn", text="Começar")
    botao_comecar.click()


#@browser_session(MOCKUP_TEST_URL_FILE, kill_browser=False)
def test_botoes(session):
    Widget(session, id="primary-btn", text="Botão Primário").click()
    mensagem_depois_click = Widget(session, id="button-click-message").properties().get("text")
    assert "Botão Primário" in mensagem_depois_click

    Widget(session, id="secondary-btn", text="Botão Secundário").click()
    mensagem_depois_click = Widget(session, id="button-click-message").properties().get("text")
    assert "Botão Secundário" in mensagem_depois_click

    Widget(session, id="danger-btn", text="Botão Perigo").click()
    mensagem_depois_click = Widget(session, id="button-click-message").properties().get("text")
    assert "Botão Perigo" in mensagem_depois_click

    disabled_btn = Widget(session, id="disabled-btn")
    assert disabled_btn.properties().get("enabled") is False

    Widget(session, text="Próximo").click()


# @browser_session(MOCKUP_TEST_URL_FILE, kill_browser=False)
def test_links(session):
    Widget(session, id="simple-link").click()
    session.accept_alert()

    Widget(session, id="new-tab-link", text="Link em Nova Aba").click()
    session.accept_alert()
    session.switch_to_new_tab()
    session.close_current_tab()

    Widget(session, id="download-link", text="Link de Download").click()
    time.sleep(0.5)
    Widget(session, text="Próximo").click()

#@browser_session(MOCKUP_TEST_URL_FILE, kill_browser=False)
def test_formularios(session):
    dummy_file_path = os.path.abspath(os.path.join(base_dir, "dummy_upload.txt"))
    with open(dummy_file_path, "w") as f:
        f.write("This is a dummy text file to test file upload.")

    try:
        Widget(session, id="text-input").enter_text("Texto de teste")
        Widget(session, id="email-input").enter_text("teste@exemplo.com")
        Widget(session, id="password-input").enter_text("senha123")
        Widget(session, id="number-input").enter_text(str(random.randint(1, 100)))
        Widget(session, id="date-input", name="date-input").enter_text("11121999")

        color_input = Widget(session, id="color-input")
        new_color = "#EEFF00"
        color_input.set_value(new_color)
        retrieved_color = color_input.get_attribute("value")
        assert retrieved_color.lower() == new_color.lower()

        file_input = Widget(session, id="file-input")
        file_input.upload_file(dummy_file_path)

        range_input = Widget(session, id="range-input")
        new_range_value = str(random.randint(1, 100))
        range_input.set_value(new_range_value)
        assert range_input.get_attribute("value") == new_range_value

        Widget(session, id="textarea-input", name="textarea-input").enter_text(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus eget nisi quam."
            )
        
        Widget(session, type="checkbox", value="opcao2").click()
        Widget(session, type="checkbox", value="opcao1").click()
        Widget(session, type="radio", value="opcao2").click()

        single_dropdown = Widget(session, id="dropdown")
        single_dropdown.scroll_to() 
        single_dropdown.select_by_text("Opção 2")
        assert single_dropdown.get_selected_texts() == ["Opção 2"]

        multi_dropdown = Widget(session, id="multi-dropdown")
        multi_dropdown.select_by_text("Opção 1")
        multi_dropdown.select_by_index(2)
        assert sorted(multi_dropdown.get_selected_texts()) == ["Opção 1", "Opção 3"]
        multi_dropdown.deselect_by_text("Opção 1")
        assert multi_dropdown.get_selected_texts() == ["Opção 3"]

        Widget(session, type="submit", id="submit-btn").click()

        form_data = Widget(session, id="form-data").properties().get("text")
        assert "dummy_upload.txt" in form_data

    finally:
        if os.path.exists(dummy_file_path):
            os.remove(dummy_file_path)
    Widget(session, text="Próximo").click()


#@browser_session(MOCKUP_TEST_URL_FILE, kill_browser=False)
def test_hover(session):
    hover_div = Widget(session, id="hover-div")
    hover_status = Widget(session, id="hover-status")
    assert "não está" in hover_status.properties().get("text")
    for _ in range(3):
        hover_div.hover()
        assert "está sobre" in hover_status.properties().get("text")
        time.sleep(0.5)
        hover_div.unhover()
        assert "não está" in hover_status.properties().get("text")
    
    Widget(session, text="Próximo").click()


#@browser_session(MOCKUP_TEST_URL_FILE, kill_browser=False)
def test_tabs(session):
    tab1_content = Widget(session, id="tab1")
    assert "primeira" in tab1_content.properties().get("text")

    Widget(session, data_tab="tab2").click()
    tab2_content = Widget(session, id="tab2")
    assert "segunda" in tab2_content.properties().get("text")

    Widget(session, data_tab="tab3").click()
    tab2_content = Widget(session, id="tab3")
    assert "terceira" in tab2_content.properties().get("text")

    Widget(session, text="Próximo").click()

#@browser_session(MOCKUP_TEST_URL_FILE, kill_browser=False)
def test_modal(session):
    Widget(session, id="open-modal-btn", text="Abrir Modal").click()
    modal = Widget(session, class_="modal", id="test-modal")

    assert "modal simples que pode ser" in modal.properties().get("text")
    assert modal.properties().get("displayed")
    
    close_btn = Widget(session, class_="close")
    assert close_btn.properties().get("displayed")
    close_btn.click()

    Widget(session, text="Próximo").click()

#@browser_session(MOCKUP_TEST_URL_FILE, kill_browser=False)
def test_alertas(session):
    Widget(session, id="success-alert-btn").click()
    alert_success = Widget(session, class_="alert alert-success")
    assert "Sucesso!" in alert_success.properties().get("text")

    Widget(session, id="warning-alert-btn").click()
    alert_warning = Widget(session, class_="alert alert-warning")
    assert "Aviso!" in alert_warning.properties().get("text")

    Widget(session, id="info-alert-btn").click()
    alert_info = Widget(session, class_="alert alert-info")
    assert "Informação!" in alert_info.properties().get("text")

    Widget(session, id="error-alert-btn").click()
    alert_error = Widget(session, class_="alert alert-danger")
    assert "Erro!" in alert_error.properties().get("text")

    Widget(session, id="toast-btn").click()
    alert_warning = Widget(session, id="toast", class_="toast show-toast")
    assert "toast!" in alert_warning.properties().get("text")

    Widget(session, text="Próximo").click()

@browser_session(MOCKUP_TEST_URL_FILE, kill_browser=False)
def test_drag_and_drop(session):
    start(session)
    test_botoes(session)
    test_links(session)
    test_formularios(session)
    test_hover(session)
    test_tabs(session)
    test_modal(session)
    test_alertas(session)

    source_drag = Widget(session, id="drag-source", draggable="true")
    target_drop = Widget(session, id="drop-target")
    status = Widget(session, id="dragdrop-status")

    assert "Nenhuma" in status.properties().get("text")
    source_drag.drag_to(target_drop)
    assert "solto" in status.properties().get("text")


if __name__ == "__main__":
    test_drag_and_drop()
    print("Todos os testes do PyAutoTk foram executados com sucesso!")