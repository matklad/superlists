#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Alice has heard about a cool TODO app. She goes to
        # check it's homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and the header to mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box.
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates and now it lists:
        # "1. By peacock feathers" as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly".
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now show both items on the list.
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn(
            '2: Use peacock feathers to make a fly',
            [row.text for row in rows]
        )


        # Alice wonders whether the site will remember her list. Then she
        # sees that the site has generated a unique URL for her --- there is
        # some explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep.
        self.browser.quit()
