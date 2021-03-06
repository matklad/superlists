#!/usr/bin/env python3
import sys
import os
import unittest
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerCase
from django.conf import settings

from .server_tools import reset_database, create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


DEFAULT_WAIT = 5
SCREEN_DUMP_LOCATION = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'screendumps')
)

class FunctionalTest(StaticLiveServerCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        if self.against_staging:
            reset_database(self.server_host)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshoting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumpling page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    def start_new_session(self):
        self.browser.quit()
        self.browser = webdriver.Firefox()

    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.server_url + '/404-no-such-url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/'
        ))

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

    def wait(self, f, timeout=DEFAULT_WAIT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return f()
            except (AssertionError, WebDriverException):
                time.sleep(.1)
            return f()

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
