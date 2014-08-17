from selenium import webdriver

from .base import FunctionalTest
from .pages import HomePage

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
        list_page = HomePage(self).start_new_list('Get help')

        # She notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # She shares her list
        list_page.share_list_with('bob@example.com')

        # Bob now goes to the lists page with his browser
        self.browser = bob_browser
        HomePage(self).visit_home().visit_my_lists()

        # He sees Alice's list in there!
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, Bob can see that it's Alice's list
        self.wait(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'alice@example.com'
        ))

        # He adds an item to the list
        list_page.add_new_item('Hi Alice')

        # When Alice refreshes the page, she sees Bob's addition
        self.browser = alice_browser
        self.browser.refresh()
        list_page.wait_for_new_item_in_list('Hi Alice', 2)
