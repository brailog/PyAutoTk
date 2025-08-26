# PyAutoTk vs. Selenium: A Side-by-Side Comparison

This document compares PyAutoTk with raw Selenium to demonstrate how PyAutoTk simplifies web automation. The core hypothesis is that PyAutoTk is easier to use, more human-friendly, and has a shorter learning curve. This makes it an excellent tool for QA testers, developers, and even non-programmers with a basic understanding of HTML and CSS.

We will analyze equivalent test cases from `playground.py` (PyAutoTk) and `playground-selenium.py` (Selenium) to highlight these differences.

## 1. Session Management and Test Execution

The first major difference is how the browser session is managed. PyAutoTk uses a simple decorator, while Selenium requires manual setup and teardown.

PyAutoTk (`playground.py`)

```python
from pyautotk.elements.helpers.session_helpers import browser_session

@browser_session(MOCKUP_TEST_URL_FILE)
def full_execution(session):
    start(session)
    test_botoes(session)
    # ... other tests
    test_drag_and_drop(session)

if __name__ == "__main__":
    full_execution()
```

Selenium (`playground-selenium.py`)

```python
from selenium import webdriver

def full_execution():
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get(MOCKUP_TEST_URL_FILE)
        start(driver)
        test_botoes(driver)
        # ... other tests
        test_drag_and_drop(driver)
    finally:
        print("Closing browser session.")
        driver.quit()

if __name__ == "__main__":
    full_execution()
```

**Compration note:**
PyAutoTk's `@browser_session` decorator abstracts away the entire browser setup and teardown process. The user only needs to specify the URL. In contrast, the Selenium code requires manually initializing the `webdriver`, using a `try...finally` block to ensure the browser is closed (`driver.quit()`), and explicitly navigating to the URL. This makes the PyAutoTk version cleaner and less prone to errors like forgetting to close the browser.

## 2. Starting the Test

Let's look at the first interaction: clicking the "start" button.

<th>PyAutoTk (<code>playground.py</code>)</th>

```python
from pyautotk.elements.widget import Widget

def start(session):
    botao_comecar = Widget(session, id="start-btn", text="Começar")
    botao_comecar.click()
```

<th>Selenium (<code>playground-selenium.py</code>)</th>

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start(driver):
    xpath = "//*[@id='start-btn' and contains(text(), 'Começar')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
```

**Compration note:**
PyAutoTk's `Widget` class allows for locating elements using simple keyword arguments like `id="start-btn"`. The code is highly readable and mirrors how one might describe the element in plain language.

The Selenium version is much more verbose. It requires:
1.  Importing `By`, `WebDriverWait`, and `expected_conditions`.
2.  Manually constructing a complex XPath string.
3.  Using `WebDriverWait` to explicitly wait for the element to be clickable before performing the action.

PyAutoTk handles these waits implicitly, making the script much cleaner.

## 3. Interacting with Buttons

This test involves clicking multiple buttons and asserting the result.

PyAutoTk (`playground.py`)

```python
def test_botoes(session):
    Widget(session, id="primary-btn", text="Botão Primário").click()
    mensagem_depois_click = Widget(session, id="button-click-message").properties().get("text")
    assert "Botão Primário" in mensagem_depois_click

    # ... (similar for other buttons)

    disabled_btn = Widget(session, id="disabled-btn")
    assert disabled_btn.properties().get("enabled") is False
```

Selenium (`playground-selenium.py`)

```python
def test_botoes(driver):
    xpath_primary = "//*[@id='primary-btn' and contains(text(), 'Botão Primário')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_primary))).click()
    message_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "button-click-message")))
    assert "Botão Primário" in message_element.text

    # ... (similar for other buttons)
    
    disabled_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "disabled-btn")))
    assert not disabled_btn.is_enabled()
```

**Compration note:**
The pattern of verbosity in Selenium continues. For each interaction, you need an explicit wait. In PyAutoTk, finding an element and acting on it is a single, readable line (e.g., `Widget(...).click()`). Getting element properties is also straightforward with `.properties()`, which returns a dictionary of useful data like `text` and `enabled` status. In Selenium, you have to call different methods like `.text` or `.is_enabled()`, and you still need to wait for the element first.

## 4. Handling Links and Tabs

This test clicks links, accepts alerts, and manages browser tabs.

PyAutoTk (`playground.py`)

```python
def test_links(session):
    Widget(session, id="simple-link").click()
    session.accept_alert()

    Widget(session, id="new-tab-link", text="Link em Nova Aba").click()
    session.accept_alert()
    session.switch_to_new_tab()
    session.close_current_tab()
```

Selenium (`playground-selenium.py`)

```python
def test_links(driver):
    original_window = driver.current_window_handle
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "simple-link"))).click()
    WebDriverWait(driver, 5).until(EC.alert_is_present()).accept()

    # ... click link that opens new tab ...
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    new_tab_handle = [handle for handle in driver.window_handles if handle != original_window][0]
    driver.switch_to.window(new_tab_handle)

    driver.close()
    driver.switch_to.window(original_window)
```

**Comparation Note:**
PyAutoTk provides high-level, descriptive methods like `accept_alert()`, `switch_to_new_tab()`, and `close_current_tab()`. These methods hide the underlying complexity.

The Selenium equivalent is much more involved. To switch to a new tab, you must:
1.  Store the original window handle.
2.  Wait for the number of windows to increase.
3.  Get the list of all window handles.
4.  Find the new handle by comparing it to the original.
5.  Manually switch to the new window.
6.  To return, you must manually switch back to the original handle.

PyAutoTk's approach is significantly more intuitive and less error-prone.

## 5. Filling Out Forms

This test covers various form inputs: text, color, file, range, checkboxes, radio buttons, and dropdowns.

PyAutoTk (`playground.py`)

```python
# Text input
Widget(session, id="text-input").enter_text("Texto de teste")

# Color input
color_input = Widget(session, id="color-input")
color_input.set_value("#EEFF00")

# File upload
Widget(session, id="file-input").upload_file(dummy_file_path)

# Range slider
range_input = Widget(session, id="range-input")
range_input.set_value("75")

# Dropdown
single_dropdown = Widget(session, id="dropdown")
single_dropdown.select_by_text("Opção 2")
assert single_dropdown.get_selected_texts() == ["Opção 2"]
```
Selenium (`playground-selenium.py`)

```python
# Text input
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "text-input"))).send_keys("Texto de teste")

# Color input
color_input = driver.find_element(By.ID, "color-input")
driver.execute_script("arguments[0].value = arguments[1];", color_input, "#EEFF00")

# File upload
file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "file-input")))
file_input.send_keys(dummy_file_path)

# Range slider
range_input = driver.find_element(By.ID, "range-input")
driver.execute_script("arguments[0].value = arguments[1]; ...", range_input, "75")

# Dropdown
from selenium.webdriver.support.ui import Select
single_dropdown_el = driver.find_element(By.ID, "dropdown")
single_select = Select(single_dropdown_el)
single_select.select_by_visible_text("Opção 2")
assert [opt.text for opt in single_select.all_selected_options] == ["Opção 2"]
```

**Comparation Note:**
PyAutoTk provides consistent, high-level methods for all form interactions. `enter_text()`, `upload_file()`, and `set_value()` are clear and concise. Dropdown interactions are built into the `Widget` class with methods like `select_by_text()` and `get_selected_texts()`.

In Selenium, the approach varies by element type. Simple text fields use `.send_keys()`, but complex inputs like color pickers and range sliders often require executing custom JavaScript. For dropdowns, you must import the `Select` class, instantiate it with the web element, and then use its methods. PyAutoTk's unified API makes the learning curve much gentler.

## 6. Hover Actions

This test checks if a message appears when hovering over an element.

PyAutoTk (`playground.py`)

```python
hover_div = Widget(session, id="hover-div")
hover_div.hover()
# ... assert text ...
hover_div.unhover()
```
Selenium (`playground-selenium.py`)

```python
from selenium.webdriver.common.action_chains import ActionChains

hover_div = driver.find_element(By.ID, "hover-div")
body = driver.find_element(By.TAG_NAME, "body")

ActionChains(driver).move_to_element(hover_div).perform()
# ... assert text ...
ActionChains(driver).move_to_element(body).perform()
```

**Compration Note:**
PyAutoTk simplifies this to a single `.hover()` method. The `.unhover()` method is also provided for convenience, which moves the mouse to a neutral area.

Selenium requires using `ActionChains`, which adds complexity. You have to build a sequence of actions (`move_to_element`) and then call `.perform()`. To "unhover," you must manually find another element (like the `<body>`) to move the mouse to.

## 7. Drag and Drop

This test demonstrates dragging one element onto another.

**PyAutoTk (`playground.py`)**
```python
source_drag = Widget(session, id="drag-source", draggable="true")
target_drop = Widget(session, id="drop-target")

source_drag.drag_to(target_drop)
```

**Selenium (`playground-selenium.py`)**

```python
source_drag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "drag-source")))
target_drop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "drop-target")))

ActionChains(driver).drag_and_drop(source_drag, target_drop).perform()
```

**Compration Note:**
PyAutoTk provides a highly intuitive `drag_to()` method. You simply tell the source widget to drag itself to the target widget. This is a perfect example of a human-friendly API.

The Selenium version again relies on `ActionChains` and is more verbose, requiring the user to find both elements first and then pass them to the `drag_and_drop` method. Furthermore, PyAutoTk's implementation handles browser-specific inconsistencies (like the need for JavaScript-based drag-and-drop in Firefox) under the hood, which is a significant advantage.

## 8. Handling Modals and Alerts

This section covers dynamic UI elements like modals and alerts.

PyAutoTk (`playground.py`)

```python
# Modal
Widget(session, id="open-modal-btn").click()
modal = Widget(session, class_="modal", id="test-modal")
assert modal.properties().get("displayed")
Widget(session, class_="close").click()

# Alerts
Widget(session, id="success-alert-btn").click()
alert_success = Widget(session, class_="alert alert-success")
assert "Sucesso!" in alert_success.properties().get("text")
```

Selenium (`playground-selenium.py`) 

```python
# Modal
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "open-modal-btn"))).click()
modal_xpath = "//*[@class='modal' and @id='test-modal']"
modal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, modal_xpath)))
assert modal.is_displayed()
driver.find_element(By.CLASS_NAME, "close").click()

# Alerts
driver.find_element(By.ID, "success-alert-btn").click()
alert_success = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success")))
assert "Sucesso!" in alert_success.text
```

**Explanation:**
PyAutoTk's syntax remains consistent and clean. Locating the modal or the alert uses the same `Widget` constructor. The Selenium code requires constructing XPaths or CSS selectors and wrapping every lookup in a `WebDriverWait` to handle the asynchronous nature of these elements appearing on the screen. PyAutoTk's implicit waits make the code much more streamlined.

---

Across all test cases, PyAutoTk consistently offers a simpler, more readable, and more intuitive API than raw Selenium.

-   **Reduced Boilerplate:** No need for explicit waits, `By` locators, or `ActionChains` in most cases.
-   **Human-Readable Locators:** `Widget(id="...", text="...")` is far clearer than complex XPaths or CSS selectors.
-   **High-Level Abstractions:** Complex actions like tab management, dropdown selection, and drag-and-drop are handled by simple, descriptive methods.
-   **Unified API:** The `Widget` class provides a consistent way to interact with different types of elements.

These features validate the hypothesis that PyAutoTk lowers the barrier to entry for web automation, making it accessible to a broader audience without sacrificing power or flexibility.