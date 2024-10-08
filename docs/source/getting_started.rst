=========================
Getting Started with PyAutoTk
=========================

In this guide, we will show you how to get started with PyAutoTk. We'll cover installation, basic configuration, and a simple script example.

Prerequisites
=================

- Python 3.8 or later.
- Pip package manager.
- (Optional) Firefox and Chrome browsers installed if you plan to run browser-based tests.

Installation
=================
To install PyAutoTk, run the following command:

```bash
pip install pyautotk
```

This command installs the core components of PyAutoTk and its dependencies (such as Selenium).

Creating Your First Script
============================

Here is a quick script to open Google and search for "PyAutoTk":

.. code-block:: python

    from pyautotk.elements.widget import Widget
    from pyautotk.elements.helpers.session_helpers import browser_session

    @browser_session(url="https://www.google.com")
    def search_google(session, search_query="PyAutoTk"):
        search_input = Widget(session, aria_label="Search")
        search_input.enter_text(search_query)
        search_button = Widget(session, aria_label="Google Search")
        search_button.click()

    if __name__ == '__main__':
        search_google()


Save this script and Run!
