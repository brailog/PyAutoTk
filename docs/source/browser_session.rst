Browser Session
===============

``browser_session`` manages browser sessions. It initializes, configures, and automatically closes browsers used in automation tasks.

**Basic Parameters:**

- ``url``: Initial page URL.
- ``browser_type``: Browser type (default: ``chrome``).
- ``headless``: Runs the browser without a graphical interface if set to ``True``.
- ``kill_browser``: Keeps the browser open after the session finishes if set to ``False``.
- ``maximize``: Starts the session with the browser maximized if set to ``True``.


**Usage Example:**

.. code-block:: python

    from pyautotk.elements.helpers.session_helpers import browser_session

    @browser_session(url="https://google.com", browser_type="firefox", kill_browser=False)
    def run_automation(session):
        print("Session started successfully!")

    run_automation()