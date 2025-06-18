# PyAutoTk

**PyAutoTk** is a modular and extensible automation framework designed to simplify the process of creating, managing, and executing automation scripts for web platforms.

## Getting Started

You have two options to get started with PyAutoTk:

1. **Cloning the repository and installing as a developer:**

```bash
git clone https://github.com/brailog/PyAutoTk.git
cd PyAutoTk
pip install -e .
```
2. **Installing PyAutoTk from PyPI:**
```bash
pip install pyautotk
```

Once installed, you can begin using the framework to automate your web application.

## When to Use PyAutoTk?

PyAutoTk is ideal for developers and QA engineers who need a structured framework for automating:

- Web application testing
- Data scraping from web applications
- Functional testing of UI components

PyAutoTk leverages Selenium for web automation, providing a flexible and powerful way to interact with complex UI elements. As the framework evolves, there will be support for mobile platforms as well.

## How to Use PyAutoTk

Let's walk through an example to help you get started with PyAutoTk.
### Example Script

Create a new file called `pyautotk_example.py` and copy the following code:

```python
import time
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session

@browser_session(url="https://www.youtube.com/")
def watch_shorts(session, swipe_times=5):
    Widget(session, text="Shorts").click()
    pt_button_down = Widget(session, aria_label="Proximo Vídeo")
    for _ in range(swipe_times):
        pt_button_down.click()
        time.sleep(1)

watch_shorts()
```
> ⚠️ **Warning**  
> The example script provided is configured for a browser in **Portuguese (pt-BR)**.  
> To adapt it for English or other languages, ensure the text used in the `aria_label` or other attributes matches the native language of your browser.  
>
> **For instance:**  
> - In Portuguese: `"Próximo Vídeo"`  
> - In English: `"Next video"`  
>
> Update the script accordingly to avoid errors during execution.

Save the file and run the script using the following command:
```bash
python3 pyautotk_example.py
```

## Explanation of the Example

- **Importing Key Components:** The example imports `browser_session` to create a session with the browser and `Widget` to interact with UI elements.
- **`browser_session` Decorator:** This decorator is essential to open the browser and navigate to the specified URL. In this case, we navigate to YouTube to view "Shorts". Optional parameters such as browser type, headless mode, and maximization can be set globally using `config_loader`.
- **Handling Language Differences:** The example demonstrates how to handle potential language differences by creating two Widget instances — one for English (`Next video`) and another for Portuguese (`Proximo vídeo`), ensuring the script works regardless of the browser language.


### Global Configuration Example

You can configure PyAutoTk globally using the config_loader. This allows you to adjust logging levels, browser types, and other settings.
```python
from pyautotk.core.config_loader import config

config.log_level = "DEBUG"
config.browser_type = "firefox"
config.headless_mode = False
config.maximize_browser = True
```
For more details, refer to the official documentation [here](https://pyautotk.readthedocs.io/en/dev-icst/)
