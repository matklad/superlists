import time

from selenium.webdriver.support.ui import WebDriverWait

from .base import FunctionalTest

class LoginTest(FunctionalTest):

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(.5)
        self.fail('could not find window {}'.format(text_in_title))

    def wait_for(self, selector):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_css_selector(selector),
            'Could not find element "{}". Page text was {}'.format(
                selector, self.find('body').text
            )
        )

    def wait_to_be_logged_in(self):
        self.wait_for('#id_logout')
        navbar = self.find('.navbar')
        self.assertIn('alice@mockmyid.com', navbar.text)

    def wait_to_be_logged_out(self):
        self.wait_for('#id_login')
        navbar = self.find('.navbar')
        self.assertNotIn('alice', navbar.text)

    def test_login_with_persona(self):
        # Alice goes to the awesome superlists site and
        # notices a "Sign in" link for the first time.
        self.visit_home()
        self.find('#id_login').click()

        # A Persona login box appers
        self.switch_to_new_window('Mozilla Persona')

        # Alice logs in with her email address
        self.find('#authentication_email').send_keys('alice@mockmyid.com')
        self.find('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # Alice can see that she is logged in
        self.wait_to_be_logged_in()

        # Refreshing the page, she sees it's a real session login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in()

        # Terrified of this new feature, she reflexively clicks 'logout'
        self.find('#id_logout').click()
        self.wait_to_be_logged_out()

        # The logged out status also persists after a refresh
        self.browser.refresh()
        self.wait_to_be_logged_out()
