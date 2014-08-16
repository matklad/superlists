from .base import FunctionalTest

import time


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_items(self):
        # Alice goes to the home page and accidentally tires to submit
        # an empty item. She hits enter on the empty input box
        self.visit_home()
        self.find_item_input_box().send_keys('\n')

        # The page refreshes and showes an error message
        error = self.find('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # She tries again with some text for the item, which now works
        self.find_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_tabel('1: Buy milk')

        # Perversely, she submits an empty item once again
        self.find_item_input_box().send_keys('\n')

        # Alice receives a similar warning on the list page
        self.check_for_row_in_list_tabel('1: Buy milk')
        error = self.find('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling in some text.
        self.find_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_tabel('1: Buy milk')
        self.check_for_row_in_list_tabel('2: Make tea')
