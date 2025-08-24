import os
import time
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session


base_dir = os.path.dirname(os.path.abspath(__file__))
MOCKUP_TEST_URL_FILE = os.path.join(base_dir, "webpage-example", "index.html")


class Arsha:
    def __init__(self, session) -> None:
        self.session = session
        self.top_home_btn = Widget(self.session, class_="nav-link scrollto", text="Home")
        self.top_about_btn = Widget(self.session, class_="nav-link scrollto", text="About")
        self.top_service_btn = Widget(self.session, class_="nav-link scrollto", text="Services")
        self.top_portfolio_btn = Widget(self.session, class_="nav-link scrollto", text="Portfolio")
        self.top_team_btn = Widget(self.session, class_="nav-link scrollto", text="Team")
        self.top_dropdown_btn = Widget(self.session, class_="bi bi-chevron-down")
        self.top_contact_btn = Widget(self.session, class_="nav-link scrollto", text="Contact")
        self.get_started_btn = Widget(self.session, text="Get Started", class_="btn-get-started scrollto")

    def dropbox_navigate(self):
        self.top_dropdown_btn.click()
        self.top_dropdown_btn.hover()


class ArshaMainSection:
    def __init__(self, session) -> None:
        self.session = session
        self.arshe = Arsha(session)
        self.get_started_btn = Widget(self.session, text="Get Started", class_="getstarted scrollto")
        self.watch_video_btn = Widget(self.session, text="Watch Video")

    def watch_main_video(self, duration: float = 5.5) -> None:
        try:
            self.arshe.top_home_btn.click(timeout=3)  # Make sure that are in the top of the page 
        except:
            pass
        self.watch_video_btn.click()  # Click on the expected "Watch Video" button
        time.sleep(duration)
        Widget(self.session, aria_label="Close").click()


class Portfolio:
    def __init__(self, session) -> None:
        self.arshe = Arsha(session)
        self.session = session

    def switch_btn(self, btn_text: str) -> None:
        Widget(self.session, text=btn_text).click()


class ContactSection:
    def __init__(self, session) -> None:
        self.arshe = Arsha(session)
        self.session = session

    def fill_contact_form(self, **kwargs)-> None:
        self.arshe.top_contact_btn.click()
        for key, value in kwargs.items():
            self.form_control_generic = Widget(self.session, class_="form-control", name=key)
            self.form_control_generic.enter_text(value)


@browser_session(MOCKUP_TEST_URL_FILE, browser_type="firefox", kill_browser=False)
def main(session):
    arshe_home_section = ArshaMainSection(session)
    contact_section = ContactSection(session)
    portifilio_section = Portfolio(session)
    
    arshe_home_section.watch_main_video()
    data = Widget(session, class_="media-body").get_all_elements_properties()

    # Filtrar todos os valores da chave 'text'
    texts = [item['text'] for item in data if 'text' in item]

    # Exibir os textos
    for text in texts:
        print(text)

    """
    contact_section.fill_contact_form(name="Gabriel", email="g@email.com", subject="dummy", message="dummy dummy dummy dummy dummy")
    time.sleep(1)
    portifilio_section.arshe.top_portfolio_btn.click()
    for option in ["All", "Card", "App", "Web"]:
        portifilio_section.switch_btn(option)
        time.sleep(0.5)
    """

if __name__ == '__main__':
    main()