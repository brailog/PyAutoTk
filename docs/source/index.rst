===================================
Documentation of Framework PyAutoTk
===================================

Welcome to the official documentation for PyAutoTk!

PyAutoTk is a modular and extensible automation framework designed to streamline the process of creating, managing, and executing automation scripts for both web and mobile platforms. This documentation provides a comprehensive overview of how to set up, configure, and utilize the framework, along with detailed API references for the core modules and components.

.. toctree::
   :maxdepth: 2
   :caption: Content:

   introduction
   getting_started
   api_reference

Introduction
============
The `Introduction` section covers the purpose of the PyAutoTk framework, its core functionalities, and the use cases it aims to solve. Learn about the fundamental concepts, supported platforms, and architecture that make up this framework.

Getting Started
===============
The `Getting Started` section provides a step-by-step guide to help you install and configure PyAutoTk in your environment. Whether you are setting it up for the first time or looking to explore more advanced configurations, this guide will serve as your foundation.

API Reference
=============
The `API Reference` contains detailed information on the modules, classes, and methods available in PyAutoTk. Each component is documented with examples and descriptions to help you integrate and extend the framework according to your needs.

Modules Reference
=================

The following sections provide in-depth documentation for the main modules in PyAutoTk:

.. toctree::
   :maxdepth: 1
   :caption: Modules:
   :titlesonly:

   core/core_overview
   core/config_loader
   elements/widget
   elements/helpers

Modules of PyAutoTk
===================
The `Modules of PyAutoTk` section provides detailed insights into the core and toolkit modules that make up the PyAutoTk framework. This section is especially useful for developers looking to extend or customize the framework for specific use cases.

Core Module Overview
====================
The `core` module is responsible for handling the lower-level interactions with the platform-specific drivers and configurations. It includes core controllers, configuration loaders, and utility functions that abstract the complexities of interacting with the Selenium WebDriver for web automation.

Elements Module Overview
========================
The `elements` module provides the building blocks for constructing UI elements and interacting with them in your scripts. It encapsulates the logic for locating and manipulating individual UI components, such as buttons, text fields, and other widgets.

Next Steps and Advanced Usage
=============================
Explore the rest of the documentation to learn about advanced usage patterns, such as integrating with CI/CD pipelines, creating reusable Page Objects, and customizing the framework for different automation scenarios. See the `examples` directory for practical scripts that demonstrate common automation tasks.

For more information, feel free to check the GitHub repository or reach out to the community for support.
