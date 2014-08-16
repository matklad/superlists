#!/usr/bin/env python3
import sys
import unittest

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerCase


class FunctionalTest(StaticLiveServerCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def start_new_session(self):
        self.browser.quit()
        self.browser = webdriver.Firefox()

    def visit_home(self):
        self.browser.get(self.server_url)

    def find(self, selector):
        return self.browser.find_element_by_css_selector(selector)

    def find_all(self, selector):
        return self.browser.find_elements_by_css_selector(selector)

    def wait_for(self, selector):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_css_selector(selector),
            'Could not find element "{}". Page text was {}'.format(
                selector, self.find('body').text
            )
        )

    def check_for_row_in_list_tabel(self, row_text):
        table = self.find('#id_list_table')
        rows = self.find_all('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def find_item_input_box(self):
        return self.find('#id_text')

    def wait_to_be_logged_in(self, email):
        self.wait_for('#id_logout')
        navbar = self.find('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for('#id_login')
        navbar = self.find('.navbar')
        self.assertNotIn(email, navbar.text)
