## Introduction to Hextec
Hextec is a test automation framework. Designed to offer a modular and scalable approach, Hextec facilitates the creation, organization, and execution of automated tests using Pytest and Selenium. The framework's structure supports a hierarchy of fixtures, ensuring reusability and proper isolation of test resources.

### Framework Structure
Hextec is structured into three main layers:

1. **CORE:** Essential scripts and environment variables for initializing and configuring the test environment.
2. **HOOKS:** Pytest-specific configurations to customize test behavior.
3. **Projects and Suites:** Organization of test cases into projects and suites, supporting a hierarchy of fixtures for different levels of scope (global, project, suite).

### Recommended Python Version
To ensure compatibility and take advantage of the latest Python features, we recommend using Python version 3.10. This version offers a balance of stability, performance, and support for modern test automation libraries.