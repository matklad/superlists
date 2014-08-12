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

    def check_for_row_in_list_tabel(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

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

        # When she hits enter, she is taken to the new URL,
        # and now the page lists: # "1. By peacock feathers"
        # as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)
        alice_list_url = self.browser.current_url
        self.assertRegex(alice_list_url, '/lists/.+')
        self.check_for_row_in_list_tabel('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly".
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now show both items on the list.
        self.check_for_row_in_list_tabel('1: Buy peacock feathers')
        self.check_for_row_in_list_tabel('2: Use peacock feathers to make a fly')

        # Now a new user, Bob, comes along to the site

        ## clean session ##
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Bob visits the home page. There is no sign of Alice's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Bob starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Bob gets his own unique URL
        bob_list_url = self.browser.current_url
        self.assertRegex(bob_list_url, '/lists/.+')
        self.assertNotEqual(bob_list_url, alice_list_url)

        # Again, there is no trace of Alice's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)


        self.fail('Finish the test!')