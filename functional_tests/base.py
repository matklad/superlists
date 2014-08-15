#!/usr/bin/env python3
import sys
import unittest

from selenium import webdriver
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

    def check_for_row_in_list_tabel(self, row_text):
        table = self.find('#id_list_table')
        rows = self.find_all('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def visit_home(self):
        self.browser.get(self.server_url)

    def find(self, selector):
        return self.browser.find_element_by_css_selector(selector)

    def find_all(self, selector):
        return self.browser.find_elements_by_css_selector(selector)
