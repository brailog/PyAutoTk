import os
import time
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session


base_dir = os.path.dirname(os.path.abspath(__file__))
MOCKUP_TEST_URL_FILE = os.path.join(base_dir, "webpage-example", "index.html")


class Arsha:
    def __init__(self, session) -> None:
        self.session = session
        self.home_btn = Widget(self.session, class_="nav-link scrollto", text="Home")
        self.about_btn = Widget(self.session, class_="nav-link scrollto", text="About")
        self.service_btn = Widget(self.session, class_="nav-link scrollto", text="Services")
        self.portfolio_btn = Widget(self.session, class_="nav-link scrollto", text="Portfolio")
        self.team_btn = Widget(self.session, class_="nav-link scrollto", text="Team")
        self.dropdown_btn = Widget(self.session, class_="bi bi-chevron-down")
        self.contact_btn = Widget(self.session, class_="nav-link scrollto", text="Contact")
        self.get_started_btn = Widget(self.session, text="Get Started", class_="btn-get-started     scrollto")

    def dropbox_navigate(self):
        self.dropdown_btn.click()
        self.dropdown_btn.hover()


class ArshaMainSection:
    def __init__(self, session) -> None:
        self.session = session
        self.arshe = Arsha(session)
        self.get_started_btn = Widget(self.session, text="Get Started", class_="getstarted scrollto")
        self.watch_video_btn = Widget(self.session, text="Watch Video")

    def watch_main_video(self, duration: float = 5.5) -> None:
        self.arshe.home_btn.click(timeout=3)
        time.sleep(1)
        self.watch_video_btn.click()
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
        self.arshe.contact_btn.click()
        for key, value in kwargs.items():
            self.form_control_generic = Widget(self.session, class_="form-control", name=key)
            self.form_control_generic.enter_text(value)


@browser_session(MOCKUP_TEST_URL_FILE, browser_type="firefox", kill_browser=False, headless=True)
def main(session):
    arshe_home_section = ArshaMainSection(session)
    contact_section = ContactSection(session)
    portifilio_section = Portfolio(session)

    contact_section.fill_contact_form(name="Gabriel", email="g@email.com", subject="dummy", message="dummy dummy dummy dummy dummy")
    time.sleep(1)
    arshe_home_section.watch_main_video()
    time.sleep(1)
    portifilio_section.arshe.portfolio_btn.click()
    for option in ["All", "Card", "App", "Web"]:
        portifilio_section.switch_btn(option)
        time.sleep(0.5)

if __name__ == '__main__':
    main()