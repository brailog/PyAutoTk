==========================
How to Use PyAutoTk
==========================

PyAutoTk is a flexible and powerful framework that supports creating automation scripts for different platforms. In this guide, we will go through how to configure the framework, create basic scripts, and leverage the Page Object pattern to structure complex automation tasks.

Setting Up Configurations
=========================

The `config` object is used to define settings for the framework, making it easy to customize the logging level, browser type, and other configurations. Here's how you can use it:

**Example: Setting Log Level and Browser Type**

.. code-block:: python

    from pyautotk.core.config_loader import config

    # Set the logging level to "DEBUG"
    config.log_level = "DEBUG"

    # Define the browser type to use ("firefox" or "chrome")
    config.browser_type = "chrome"

In this example, we set the `log_level` to `DEBUG`, which provides detailed information during script execution. Similarly, we choose the Chrome browser for our automation.

Basic Automation Script
========================

To get started, let's create a simple automation script that navigates to Google, searches for "PyAutoTk", and clicks the search button:

.. code-block:: python

    import time
    from pyautotk.elements.widget import Widget
    from pyautotk.elements.helpers.session_helpers import browser_session

    @browser_session(url="https://www.google.com")
    def search_google(session, search_input="PyAutoTk"):
        Widget(session, aria_label="Search").enter_text(search_input)
        Widget(session, aria_label="Google Search").click()
        time.sleep(2)

    if __name__ == '__main__':
        search_google()

This script uses the `browser_session` decorator to open a browser and navigate to Google. It then interacts with the UI using `Widget` to enter a search term and click the search button.

Creating a Page Object Class
============================

The Page Object Pattern helps you create maintainable and reusable automation scripts by organizing the interactions into classes that represent different pages of your application. Let's create a `GoogleSearchPage` class to demonstrate this pattern:

.. code-block:: python

    from pyautotk.elements.widget import Widget
    from pyautotk.elements.helpers.session_helpers import browser_session

    class GoogleSearchPage:
        def __init__(self, session):
            self.search_input = Widget(session, aria_label="Search")
            self.search_button = Widget(session, aria_label="Google Search")

        def search(self, text):
            self.search_input.enter_text(text)
            self.search_button.click()

    @browser_session(url="https://www.google.com")
    def test_google_search(session, search_input="PyAutoTk"):
        search_page = GoogleSearchPage(session)
        search_page.search(search_input)

    if __name__ == '__main__':
        test_google_search()

This script demonstrates a basic Page Object class. Each `Widget` represents a component on the page, making it easy to interact with the elements using intuitive methods.

Complex Automation Flow
========================

Let's build on this pattern to create a more complex flow that involves navigating through multiple pages:

.. code-block:: python

    import time
    from pyautotk.elements.widget import Widget
    from pyautotk.elements.helpers.session_helpers import browser_session

    class YouTubeShortsPage:
        def __init__(self, session):
            self.shorts_button = Widget(session, text="Shorts")
            self.scroll_button = Widget(session, id="navigation-button-down")

        def open_shorts(self):
            self.shorts_button.click()

        def scroll_shorts(self, times=5):
            for _ in range(times):
                self.scroll_button.wait_for()
                self.scroll_button.click()
                time.sleep(1)

    @browser_session(url="https://www.youtube.com/")
    def browse_youtube_shorts(session, scroll_times=10):
        shorts_page = YouTubeShortsPage(session)
        shorts_page.open_shorts()
        shorts_page.scroll_shorts(times=scroll_times)

    if __name__ == '__main__':
        browse_youtube_shorts()

In this example, the `YouTubeShortsPage` class encapsulates the interaction logic for YouTube Shorts. The `browse_youtube_shorts` function uses this class to automate a more complex workflow.

Understanding the Configuration Options
=======================================

### `config.log_level`
Defines the level of logging for the framework. Possible values include:

- `DEBUG`: Outputs detailed information, useful for debugging.
- `INFO`: General information about the flow of the script.
- `WARNING`: Warnings that don't interrupt the script but need attention.
- `ERROR`: Errors that affect the execution.

Example:

.. code-block:: python

    from pyautotk.core.config_loader import config
    config.log_level = "INFO"

### `config.browser_type`
Specifies which browser to use for web automation. Supported values are:

- `firefox` (default)
- `chrome`

Example:

.. code-block:: python

    from pyautotk.core.config_loader import config
    config.browser_type = "chrome"

### `config.headless`
Runs the browser in headless mode if set to `True`. This is useful for running scripts in environments without a display.

Example:

.. code-block:: python

    from pyautotk.core.config_loader import config
    config.headless = True

Putting It All Together
=======================

Here's a more complete example that uses all the features described above:

.. code-block:: python

    import time
    from pyautotk.elements.widget import Widget
    from pyautotk.elements.helpers.session_helpers import browser_session
    from pyautotk.core.config_loader import config

    # Setting up configurations
    config.log_level = "DEBUG"
    config.browser_type = "chrome"
    config.headless = False

    @browser_session(url="https://www.google.com")
    def search_google(session, search_input="PyAutoTk"):
        search_input_widget = Widget(session, aria_label="Search")
        search_input_widget.enter_text(search_input)
        search_button = Widget(session, aria_label="Google Search")
        search_button.click()
        time.sleep(2)

    if __name__ == '__main__':
        search_google()

This script configures the framework, navigates to Google, performs a search, and logs each step using the defined configurations.
