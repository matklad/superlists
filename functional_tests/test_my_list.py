from .base import FunctionalTest


class MyListTest(FunctionalTest):

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
        self.wait(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

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
