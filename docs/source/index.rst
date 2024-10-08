===================================
PyAutoTk Framework Documentation
===================================

Welcome to the official documentation for PyAutoTk!

PyAutoTk is a powerful and extensible framework designed to make it easier to create, manage, and execute automation scripts across web and mobile platforms. This documentation serves as a comprehensive guide to help you get started with PyAutoTk, configure its settings, and use its various components to build robust automation solutions.

.. toctree::
   :maxdepth: 2
   :caption: Quick Start Guide:

   introduction
   getting_started

Quick Start Guide
=================
The `Quick Start Guide` helps you set up and run your first script using PyAutoTk. This section introduces the core concepts, provides step-by-step installation instructions, and walks through a simple example to get you up and running quickly.

Configuration Options
======================
PyAutoTk offers flexible configurations to adjust the behavior of the framework to your needs. Learn how to use the `config` object to set logging levels, define browser types, and control other options:

**Example: Setting Log Level and Browser Type**

.. code-block:: python

   from pyautotk.core.config_loader import config

   # Set the logging level to "DEBUG"
   config.log_level = "DEBUG"

   # Define the browser type to use ("firefox" or "chrome")
   config.browser_type = "chrome"

Modules Overview
================
PyAutoTk is structured into various modules, each responsible for a specific aspect of automation. Below is an overview of the key modules:

- **Core Module**: Contains low-level controllers and configuration utilities.
- **Elements Module**: Encapsulates logic for interacting with UI elements, such as buttons and input fields, using the Page Object Pattern.
- **Helpers Module**: Provides utility functions and decorators to simplify session management and code organization.

API Reference
=============
The `API Reference` provides detailed information on the modules, classes, and methods available in PyAutoTk. Each component is documented with descriptions and examples to help you integrate the framework efficiently into your own scripts.

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   core/core_overview
   core/config_loader
   elements/widget
   elements/helpers

Examples and Use Cases
======================
Explore real-world examples and use cases that demonstrate how to apply PyAutoTk in various scenarios, from simple UI interactions to advanced workflows using the Page Object Pattern. See the `examples` directory for practical scripts.

**Example: YouTube Shorts Automation**

The script below navigates to YouTube, opens the Shorts section, and scrolls through multiple shorts:

.. code-block:: python

   import time
   from pyautotk.elements.widget import Widget
   from pyautotk.elements.helpers.session_helpers import browser_session
   from pyautotk.core.config_loader import config

   config.log_level = "DEBUG"
   config.browser_type = "chrome"

   @browser_session(url="https://www.youtube.com/")
   def watch_shorts(session, swipe_times=5):
       Widget(session, text="Shorts").click()
       button_down = Widget(session, id="navigation-button-down")
       for swipe in range(swipe_times):
           button_down.wait_for()
           button_down.click()
           time.sleep(1)

   if __name__ == '__main__':
       watch_shorts()

**Check out more in the Examples section to see how you can leverage the full power of PyAutoTk!**

======================
Community and Support
======================

For more information and resources, check out the links below:

- **Source Code**: The full source code is available on [GitHub](https://github.com/brailog/PyAutoTk).
- **Report an Issue**: If you encounter any issues, feel free to submit them on our [GitHub Issues page](https://github.com/brailog/PyAutoTk/issues).
- **Documentation**: Read the documentation online at [ReadTheDocs](https://pyautotk.readthedocs.io).
- **Contributing**: Contributions are welcome! Please see our [Contributing Guidelines](https://github.com/brailog/PyAutoTk/blob/main/CONTRIBUTING.md) for more details.

Stay connected and join the discussion to help improve PyAutoTk for everyone!

----------------------

For more examples and tutorials, visit the `examples` directory on the [GitHub repository](https://github.com/brailog/PyAutoTk/tree/main/pyautotk/examples).
