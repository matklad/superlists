from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()


class MyListTest(FunctionalTest):

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

    def test_logged_in_user_lists_are_saved_as_my_lists(self):
        # Alice is a logged in user
        self.create_pre_authenticated_session('alice@example.com')

        # She goes to the home page and starts a list
        self.visit_home()
        self.find_item_input_box().send_keys('Reticulate splines\n')
        self.find_item_input_box().send_keys('Immanetize eshaton\n')
        first_list_url = self.browser.current_url

        # Alice notices a "My lists" link, for the first time.
        self.browser.find_element_by_link_text('My lists').click()

        # Browser gets her to a new page, titled My Lists
        self.assertEqual(self.find('h1').text, "My Lists")

        # She sees that her list is there, named according to its
        # first item
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.assertEqual(self.browser.current_url, first_list_url)

        # She decides to add another list, just to see
        self.visit_home()
        self.find_item_input_box().send_keys('Click cookies\n')
        second_list_url = self.browser.current_url

        # Under "my lists" her new list appears
        self.browser.find_element_by_link_text('My lists').click()
        self.browser.find_element_by_link_text('Click cookies').click()
        self.assertEqual(self.browser.current_url, second_list_url)

        # She logs out. The "My lists" option disappears
        self.find('#id_logout').click()
        self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        )
