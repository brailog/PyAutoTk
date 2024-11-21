Configuration
=============

PyAutoTk allows customization of behavior through the ``config`` module.

**Example Configuration:**

.. code-block:: python

    from pyautotk.core.config_loader import config

    config.browser_type = "firefox"
    config.headless_mode = True
    config.maximize_browser = True

These settings apply globally across the library, ensuring consistency in all scripts.
