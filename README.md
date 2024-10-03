# PyAutoTk

PyAutoTk is a modular, extensible Python framework designed to facilitate the automation of applications across different platforms, such as web browsers and Android devices. The framework follows a layered architecture that promotes a clear separation of concerns, making it easy to manage, expand, and refactor.

With PyAutoTk, you can create sophisticated automation scripts using a combination of platform-specific controllers and a toolkit layer that abstracts the complexity of UI interactions, allowing for seamless development of automated tests or interaction scripts.
Key Features

- Cross-Platform Support: The framework supports both web and mobile automation, with controllers tailored for Selenium (browser) and UIAutomator (Android).
- Layered Design: The architecture is separated into Controller and Toolkit layers, promoting modularity and reducing code duplication.
- Reusable Components: Use pre-built Widgets, Screens, and Utilities for common UI interactions.
- Centralized Logging: Integrated Logger module for comprehensive logging and debugging.
- Resource Management: Easy handling of external resources such as JSON, CSV, images, and HTML templates.
- Page Object Pattern: Built-in support for structured automation flows using the Page Object Pattern, simplifying complex interaction models.
- Scalable and Extensible: Designed to be easily extended to support additional platforms or new UI components.

## Architecture Overview

The architecture is built around two primary layers: Controller and Toolkit, with additional support modules for logging and resources.
1. Controller Layer

The Controller Layer handles the communication with different platforms, such as web browsers and Android devices. It abstracts the complexity of each platform's automation tools (e.g., Selenium for web and UIAutomator for Android) and provides a unified interface for higher-level components in the framework to interact with.

### Key Components:

- BaseController: Defines common interfaces and functionalities shared between different controllers.
- BrowserController: Manages interactions with web applications using Selenium.
- AndroidController: Manages interactions with Android devices using UIAutomator.

2. Toolkit Layer

The Toolkit Layer serves as the core component library of the framework, containing all the building blocks required for creating robust automation scripts. It includes Widgets, Screens, and Utility functions that rely on the Controller Layer for platform-specific interactions.

### Key Components:

- Widgets: Individual UI elements such as buttons, text inputs, and dropdowns, encapsulated in reusable classes.
- Screens: Implementations of the Page Object Pattern to organize interactions with complex interfaces, making scripts more readable and maintainable.
- Utilities: Helper functions and classes for handling common operations like string manipulation, waiting for elements, and dealing with data formats.

## Getting Started

To get started with PyAutoTk, follow these basic steps:

- Installation: Install the package from PyPI.

´´´bash
pip install pyautotk
´´´

- Configure Controllers: Depending on your target platform, initialize the appropriate controller (e.g., BrowserController for web or AndroidController for mobile).
- Create a Screen: Use the Toolkit layer to define screens and their associated widgets using the Page Object Pattern.
- Develop Scripts: Build scripts that utilize the defined screens, interact with widgets, and leverage the logging and resource management capabilities.

## Example Usage

Below is a basic example of how to set up a screen and automate a simple login scenario:

Define the Login Screen: Define a LoginScreen class using the Screen and Widget components from the Toolkit layer. This class will represent the login page of your application, making it easy to interact with the login fields and buttons.

Implement Automation Flow: Utilize the BrowserController to interact with the login screen, inputting values, clicking buttons, and validating results.


## License

PyAutoTk is licensed under the MIT License. See the LICENSE file for more details.
Community and Support

For questions, support, or to share ideas, feel free to open an issue on GitHub. We welcome discussions and collaborations to help improve the framework and expand its capabilities.
