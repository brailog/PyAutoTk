
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
MOCKUP_TEST_URL_FILE = os.path.join(base_dir, "playground.html")


@browser_session(f"file://{MOCKUP_TEST_URL_FILE}")
def test_botoes(session):
    Widget(session, id="primary-btn", text="Botão Primário").click()
    message = Widget(session, id="button-click-message").properties().get("text")
    assert "Botão Primário" in message

    Widget(session, id="secondary-btn", text="Botão Secundário").click()
    disabled_btn = Widget(session, id="disabled-btn")
    assert disabled_btn.properties().get("enabled") is False
    
@browser_session(f"file://{MOCKUP_TEST_URL_FILE}")
def test_formularios(session):
    for _ in range(2):
        Widget(session, id="next-btn").click()

    Widget(session, id="text-input").enter_text("Texto de teste")
    Widget(session, id="email-input").enter_text("teste@exemplo.com")
    Widget(session, id="password-input").enter_text("senha123")
    Widget(session, id="number-input").enter_text("42")
    Widget(session, id="radio2").click()
    Widget(session, text="Opção 2").click()
    Widget(session, id="submit-btn").click()
    
    form_data = Widget(session, id="form-data").properties().get("text")
    assert "teste@exemplo.com" in form_data
    assert "senha123" in form_data

@browser_session(f"file://{MOCKUP_TEST_URL_FILE}")
def test_hover(session):
    for _ in range(3):
        Widget(session, id="next-btn").click()

    hover_div = Widget(session, id="hover-div")
    hover_status = Widget(session, id="hover-status")
    assert "não está" in hover_status.properties().get("text")
    hover_div.hover()
    assert "está sobre" in hover_status.properties().get("text")

@browser_session(f"file://{MOCKUP_TEST_URL_FILE}")
def test_tabs(session):
    for _ in range(4):
        Widget(session, id="next-btn").click()

    tab1_content = Widget(session, id="tab1")
    assert "primeira" in tab1_content.properties().get("text")
    tab2_btn = Widget(session, data_tab="tab2")
    tab2_btn.click()
    tab2_content = Widget(session, id="tab2")
    assert "segunda" in tab2_content.properties().get("text")


@browser_session(f"file://{MOCKUP_TEST_URL_FILE}")
def test_modal(session):
    for _ in range(5):
        Widget(session, id="next-btn").click()

    open_modal_btn = Widget(session, id="open-modal-btn")
    open_modal_btn.click()
    modal = Widget(session, id="test-modal")
    assert modal.properties().get("displayed")
    close_btn = Widget(session, text="Fechar")
    assert close_btn.properties().get("displayed")
    close_btn.click()
    assert not modal.properties().get("displayed")

@browser_session(f"file://{MOCKUP_TEST_URL_FILE}")
def test_alertas(session):
    for _ in range(6):
        Widget(session, id="next-btn").click()

    success_btn = Widget(session, id="success-alert-btn")
    success_btn.scroll_to()
    success_btn.click()
    alert_success = Widget(session, class_="alert alert-success")
    assert "Sucesso!" in alert_success.properties().get("text")

    warning_btn = Widget(session, id="warning-alert-btn")
    warning_btn.click()
    alert_warning = Widget(session, class_="alert alert-warning")
    assert "Aviso!" in alert_warning.properties().get("text")


if __name__ == "__main__":
    test_botoes()
    #test_links()
    test_formularios()
    test_hover()
    test_tabs()
    test_modal()
    test_alertas()
    print("Todos os testes do PyAutoTk foram executados com sucesso!")