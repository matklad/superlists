#!/usr/bin/env python3
from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Alice has heard about a cool TODO app. She goes to
        # check it's homepage.
        self.browser.get('http://localhost:8000')

        # She notices the page title and the header to mention to-do lists.
        self.assertIn('To-do', self.browser.title)
        self.fail('Finish the test')

        # She is invited to enter a to-do item straight away.

        # She types "Buy peacock feathers" into a text box.

        # When she hits enter, the page updates and now it lists:
        # "1. By peacock feathers" as an item in a to-do list.

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly".

        # The page updates again, and now show both items on the list.

        # Alice wonders whether the site will remember her list. Then she
        # sees that the site has generated a unique URL for her --- there is
        # some explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep.
        self.browser.quit()

if __name__ == "__main__":
    unittest.main(warnings='ignore')
