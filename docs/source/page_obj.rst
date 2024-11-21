Page Object
===========

**What is a Page Object?**

Page Object Model (POM) is a design pattern that promotes separation of concerns. Instead of defining actions directly in scripts, you encapsulate logic in classes that represent pages or UI components.

Practical Example with PyAutoTk
-------------------------------
Using the provided local template, let’s automate a contact form:

.. code-block:: python

    class ContactPage:
        def __init__(self, session):
            self.name_field = Widget(session, name="name")
            self.email_field = Widget(session, name="email")
            self.subject_field = Widget(session, name="subject")
            self.message_field = Widget(session, name="message")
            self.submit_button = Widget(session, text="Send Message")

        def fill_contact_form(self, name, email, subject, message):
            self.name_field.enter_text(name)
            self.email_field.enter_text(email)
            self.subject_field.enter_text(subject)
            self.message_field.enter_text(message)
            self.submit_button.click()

Using in a Script:
~~~~~~~~~~~~~~~~~~
.. code-block:: python

    from pyautotk.elements.helpers.session_helpers import browser_session
    from contact_page import ContactPage

    @browser_session(url="file://local_path_to_template.html")
    def test_contact_form(session):
        contact = ContactPage(session)
        contact.fill_contact_form(
            name="John Doe",
            email="john@example.com",
            subject="Feedback",
            message="I love PyAutoTk!"
        )

    test_contact_form()

.. tip::

   You can clone the PyAutoTk repository to access a fully functional example page along with pre-structured Page Object implementations. This example is located at the following path:

   `PyAutoTk Examples <https://github.com/brailog/PyAutoTk/tree/page-obj/pyautotk/examples>`_

   The repository provides:

   - A sample webpage for testing automation.
   - A ready-to-use Page Object structure.
   - Example scripts demonstrating how to interact with the library.

   Cloning the repository is a great way to quickly get started and explore the full potential of PyAutoTk in a practical setting.
