from .base import FunctionalTest


class LayoutAndStyleTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.visit_home()
        self.browser.set_window_size(1024, 768)

        inputbox = self.find_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        inputbox.send_keys('testing\n')
        inputbox = self.find_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
