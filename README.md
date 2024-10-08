# PyAutoTk

Welcome to the PyAutoTk documentation!
PyAutoTk is a modular and extensible automation framework designed to simplify the process of creating, managing, and executing automation scripts for both web and mobile platforms. The framework is built around the Page Object Model pattern and provides a rich set of tools for building automation scripts that are easy to maintain, read, and expand.

### Key features of PyAutoTk:
- `Cross-Platform Support:` The framework supports both web and mobile automation (Android support coming soon!).
- `Layered Architecture:` Separate the control logic from the UI elements using Controllers and Toolkits.
- `Page Object Pattern:` Simplify your automation flows by using the industry-standard Page Object Pattern.
- `High Customizability:` Easily extend and configure the framework to suit your specific needs.

## When to Use PyAutoTk?

PyAutoTk is ideal for developers and QA engineers who need a structured framework for automating:

- Web application testing
- Data scraping from web applications
- Functional testing of UI components

PyAutoTk leverages Selenium for web automation, providing a flexible and powerful way to interact with complex UI elements. Stay tuned as we continue to expand support for mobile platforms.

## How PyAutoTk Works

The framework follows a layered architecture that promotes separation of concerns and modularity. PyAutoTk provides the following key modules:

- `Core Module:` Manages the browser session and handles platform-specific configurations.
- `Elements Module:` Contains components like Widget for interacting with UI elements.
- `Helpers Module:` Provides utilities and decorators for session management.

### Example: Getting Started with a Simple Script

The script below demonstrates a basic use of PyAutoTk to automate a Google Search.

```python
from pyautotk.elements.widget import Widget
from pyautotk.elements.helpers.session_helpers import browser_session
from pyautotk.core.config_loader import config

# Configure the framework
config.log_level = "DEBUG"
config.browser_type = "chrome"

@browser_session(url="https://www.google.com")
def search_google(session, search_query="PyAutoTk"):
    search_input = Widget(session, aria_label="Search")
    search_input.enter_text(search_query)
    search_button = Widget(session, aria_label="Google Search")
    search_button.click()
```

## Community and Support

For more information and resources, check out the links below:
- [Documentation on ReadTheDocs:](https://pyautotk.readthedocs.io/en/latest/) Read the complete documentation online.

For more examples and tutorials, visit the `examples` directory on the [GitHub repository](https://github.com/brailog/PyAutoTk/tree/main/pyautotk/examples).
