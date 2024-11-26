Getting Started
===============

Requirements
------------
- Python 3.6 or higher.
- Installed compatible browsers (Chrome, Firefox).

Supported Platforms:
--------------------
- **Operating Systems:** Windows 10, Windows 11, Ubuntu 16.04 or newer.
- **Browsers:** Firefox and Chrome (Chrome is the default browser).

Installation
------------
Install directly from PyPI::

    pip install pyautotk

Or install from the repository::

    git clone https://github.com/brailog/PyAutoTk.git
    cd pyautotk
    pip install -e .

Example Code
------------
.. code-block:: python

   import time
   from pyautotk.elements.widget import Widget
   from pyautotk.elements.helpers.session_helpers import browser_session


   @browser_session(url="https://www.youtube.com/")
   def watch_shorts(session, swipe_times=5):
      Widget(session, text="Shorts").click()
      pt_button_down = Widget(session, aria_label="Proximo Vídeo")
      for _ in range(swipe_times):
         pt_button_down.wait_for()
         pt_button_down.click()
         time.sleep(1)

    watch_shorts()

.. attention::

   The example script provided is configured for a browser in Portuguese (pt-BR). 
   To adapt it for English or other languages, ensure the text used in the `aria_label` 
   or other attributes matches the native language of your browser.

   For instance:
   - In Portuguese: ``"Próximo Vídeo"``
   - In English: ``"Next video"``

   Update the script accordingly to avoid errors during execution.
