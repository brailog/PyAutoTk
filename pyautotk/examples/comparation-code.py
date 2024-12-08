import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session

# Configuração de diretórios
base_dir = os.path.dirname(os.path.abspath(__file__))
MOCKUP_TEST_URL_FILE = os.path.join(base_dir, "webpage-example", "index.html")
output_csv = os.path.join(base_dir, "performance_comparison.csv")


@browser_session(MOCKUP_TEST_URL_FILE, browser_type="firefox", headless=True)
def pyauto_fill_contact_form(session, **kwargs) -> (float, float):
    start_mem = get_memory_usage()
    start_time = time.time()
    Widget(session, class_="nav-link scrollto", text="Contact").click()

    for key, value in kwargs.items():
        form_control_generic = Widget(session, class_="form-control", name=key)
        form_control_generic.enter_text(value)

    elapsed_time = time.time() - start_time
    end_mem = get_memory_usage()
    print(f"PyAutoTk Test Duration: {format_time_difference(elapsed_time)} seconds")
    print(f"Memory Used: {end_mem - start_mem:.3f} MB")
    return elapsed_time, end_mem - start_mem


def fill_contact_form(name, email, subject, message) -> (float, float):
    start_mem = get_memory_usage()
    driver = webdriver.Firefox(service=FirefoxService())
    driver.get(f"file:///{MOCKUP_TEST_URL_FILE}")
    start_time = time.time()

    contact = driver.find_element(By.XPATH, "//a[contains(@class, 'nav-link') and contains(@class, 'scrollto') and text()='Contact']")
    contact.click()

    form_element = driver.find_element(By.XPATH, '//form[@class="php-email-form"]')
    driver.execute_script("arguments[0].scrollIntoView();", form_element)

    name_field = driver.find_element(By.ID, "name")
    name_field.send_keys(name)
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys(email)

    subject_field = driver.find_element(By.ID, "subject")
    message_field = driver.find_element(By.TAG_NAME, "textarea")

    subject_field.send_keys(subject)
    message_field.send_keys(message)

    elapsed_time = time.time() - start_time
    end_mem = get_memory_usage()
    print(f"Selenium Test Duration: {format_time_difference(elapsed_time)} seconds")
    print(f"Memory Used: {end_mem - start_mem:.3f} MB")
    driver.quit()
    return elapsed_time, end_mem - start_mem


def compare_performance():
    pyautotk_times = []
    pyautotk_memory = []
    selenium_times = []
    selenium_memory = []

    # Rodar múltiplas execuções
    iterations = 10
    for i in range(iterations):
        print(f"\nIteration {i+1}: Running PyAutoTk test...")
        pyautotk_time, pyautotk_mem = pyauto_fill_contact_form(
            name="Gabriel", 
            email="g@email.com", 
            subject="dummy", 
            message="dummy dummy dummy dummy dummy"
        )
        pyautotk_times.append(pyautotk_time)
        pyautotk_memory.append(pyautotk_mem)
        time.sleep(1.5)

        print(f"\nIteration {i+1}: Running Selenium test...")
        selenium_time, selenium_mem = fill_contact_form(
            name="Gabriel", 
            email="g@email.com", 
            subject="dummy", 
            message="dummy dummy dummy dummy dummy"
        )
        selenium_times.append(selenium_time)
        selenium_memory.append(selenium_mem)

    # Estatísticas
    results = {
        "Iteration": list(range(1, iterations + 1)),
        "PyAutoTk Time (s)": pyautotk_times,
        "PyAutoTk Memory (MB)": pyautotk_memory,
        "Selenium Time (s)": selenium_times,
        "Selenium Memory (MB)": selenium_memory,
    }

    # Salvar dados detalhados
    df_detailed = pd.DataFrame(results)
    df_detailed.to_csv(output_csv, index=False)
    print(f"\nDetailed Results saved to {output_csv}")


def format_time_difference(timestamp: float) -> str:
    milliseconds = int((timestamp % 1) * 1000)
    seconds = int(timestamp % 60)
    minutes = int((timestamp // 60) % 60)
    hours = int(timestamp // 3600)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


if __name__ == "__main__":
    compare_performance()
