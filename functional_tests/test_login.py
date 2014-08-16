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
            lambda b: b.find_element_by_css_selector(selector)
        )

    def test_login_with_persona(self):
        # Alice goes to the awesome superlists site and
        # notices a "Sign in" link for the first time.
        self.visit_home()
        self.find('#login').click()

        # A Persona login box appers
        self.switch_to_new_window('Mozilla Persona')

        # Alice logs in with her email address
        self.find('#authentication_email').send_keys('alice@mockmyid.com')
        self.find('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # Alice can see that she is logged in
        self.wait_for('#logout')
        navbar = self.find('.navbar')
        self.assertIn('alice@mockmyid.com', navbar.text)
