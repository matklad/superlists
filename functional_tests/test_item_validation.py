from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_items(self):
        # Alice goes to the home page and accidentally tires to submit
        # an empty item. She hits enter on the empty input box

        # The page refreshes and showes an error message

        # She tries again with some text for the item, which now works

        # Perversely, she submits an empty item once again

        # Alice receives a similar warning on the list page

        # And she can correct it by filling in some text.
        self.fail('write me!')
