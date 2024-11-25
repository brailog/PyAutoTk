Widget
======

Widgets represent UI elements on a web page. They simplify basic interactions such as clicking, typing, and scrolling without requiring complex XPath definitions.

**Key Widget Actions:**

- ``click``: Click on an element.
- ``enter_text``: Type text into input fields.
- ``scroll_to``: Scroll to make an element visible.
- ``wait_for``: Wait until an element becomes visible.
- ``get_element_properties``: Retrieves the properties of a single element that matches the given XPath, including attributes, text and visibility status.
- ``get_all_elements_properties``: Retrieves the properties of all elements that match the given XPath, including attributes, text, and visibility status.

**Basic Example**

.. code-block:: python

    from pyautotk.elements.widget import Widget
    from pyautotk.elements.helpers.session_helpers import browser_session
    import time

    @browser_session(url="https://www.google.com")
    def search_google(session, search_input: str):
        Widget(session, aria_label="Pesquisar").enter_text(search_input)
        Widget(session, aria_label="Pesquisa Google").click()
        time.sleep(1)

    search_google("Arcane")

.. warning::  
   Update the script accordingly to your browser language to avoid errors during execution.
