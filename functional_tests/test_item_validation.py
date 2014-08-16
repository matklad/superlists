from .base import FunctionalTest

import time


class ItemValidationTest(FunctionalTest):

    def find_error(self):
        return self.find('.has-error')

    def test_cannot_add_empty_items(self):
        # Alice goes to the home page and accidentally tires to submit
        # an empty item. She hits enter on the empty input box
        self.visit_home()
        self.find_item_input_box().send_keys('\n')

        # The page refreshes and showes an error message
        error = self.find_error()
        self.assertEqual(error.text, "You can't have an empty list item")

        # She tries again with some text for the item, which now works
        self.find_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_tabel('1: Buy milk')

        # Perversely, she submits an empty item once again
        self.find_item_input_box().send_keys('\n')

        # Alice receives a similar warning on the list page
        self.check_for_row_in_list_tabel('1: Buy milk')
        error = self.find_error()
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling in some text.
        self.find_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_tabel('1: Buy milk')
        self.check_for_row_in_list_tabel('2: Make tea')

    def test_cannot_submit_duplicate_items(self):
        # Alice goes to the home page and starts a new list
        self.visit_home()
        self.find_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_tabel('1: Buy milk')

        # She accidentally tries to submit the same item again
        self.find_item_input_box().send_keys('Buy milk\n')

        # And Alice sees a helpfull error message
        self.check_for_row_in_list_tabel('1: Buy milk')
        self.assertEqual(
            self.find_error().text,
            "You've already got this item in your list"
        )

    def tests_errors_are_cleared_on_input(self):
        # Alice starts a new list in a way that causes validation error
        self.visit_home()
        self.find_item_input_box().send_keys('\n')

        # She sees a pretty error message
        error = self.find_error()
        self.assertTrue(error.is_displayed())

        # She starts typing in the input box to submit and item
        self.find_item_input_box().send_keys('B')

        # Alice is pleased to see that the error message disappers
        error = self.find_error()
        self.assertFalse(error.is_displayed())
