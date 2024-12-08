from pyautotk.elements.helpers.session_helpers import browser_session
from pyautotk.elements.widget import Widget
from unittest.mock import MagicMock
import unittest

class TestWidgetXPath(unittest.TestCase):
    def setUp(self):
        self.controller = MagicMock()

    def test_generate_xpath_single_attribute(self):
        widget = Widget(self.controller, id="submit-btn")
        expected_xpath = "//*[@id='submit-btn']"
        self.assertEqual(
            widget.xpath,
            expected_xpath,
            "XPath generation failed for single attribute.",
        )

    def test_generate_xpath_multiple_attributes(self):
        widget = Widget(self.controller, id="submit-btn", class_name="btn-primary", text="Submit")
        expected_xpath = (
            "//*[@id='submit-btn' and @class='btn-primary' and contains(text(), 'Submit')]"
        )
        self.assertEqual(
            widget.xpath,
            expected_xpath,
            "XPath generation failed for multiple attributes.",
        )

if __name__ == '__main__':
    unittest.main()
