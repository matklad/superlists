from selenium import webdriver

from .base import FunctionalTest

def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass

class SharingTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Alice is a logged-in user
        self.create_pre_authenticated_session('alice@example.com')
        alice_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(alice_browser))

        # Her friend Bob is also hanging out on the lists site
        bob_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(bob_browser))
        self.browser = bob_browser
        self.create_pre_authenticated_session('bob@example.com')

        # Alice goes to the home page and starts a list
        self.browser = alice_browser
        self.visit_home()
        self.find_item_input_box().send_keys('Get help\n')

        # She notices a "Share this list" option
        share_box = self.find('input[name=email]')
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )
