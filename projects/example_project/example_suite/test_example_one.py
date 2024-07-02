from controllers.browser.browser_controller import BrowserController
from controllers.browser.widget import Widget


def test_example_one(browser_controller: 'BrowserController'):
    browser = browser_controller
    browser.open_url("https://www.linkedin.com/")

    #btn_login = Widget(browser.driver, data_tracking_will_navigate="Sign in")
    btn_login = Widget(browser.driver, text="Sign in")
    btn_username_login = Widget(browser.driver, id="username", name="session_key", type="text")
    btn_password_login = Widget(browser.driver, id="password", name="session_password", type="password")
    btn_login.click()
    btn_username_login.click()
    btn_username_login.enter_text("defaultusertest99@gmail.com")
    btn_password_login.click()
    btn_password_login.enter_text("test3227")
    btn_login = Widget(browser.driver, text="Sign in", type="submit")
    btn_login.click()

    # search = Widget(browser.driver, placeholder="Search", type="text")
    # search.click(timeout=30)
    # search.enter_text("Empreendedorismo")
    # search_input = search.get_input
    # search_input.press_enter()
    #
    # #btn_people = Widget(browser.driver, class_="search-navigation", text="People")
    # #btn_people.click()
    # btn_see_all_people = Widget(browser.driver, text="See all people results")
    # btn_see_all_people.scroll_to()
    # btn_see_all_people.click()
    # print(Widget.get_all_elements_with_attribute(browser.driver, "href"))
