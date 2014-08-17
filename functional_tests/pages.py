class Page(object):

    def __init__(self, test):
        self.test = test

class HomePage(Page):

    def visit_home(self):
        self.test.browser.get(self.test.server_url)
        self.test.wait(self.get_item_input)
        return self

    def get_item_input(self):
        return self.test.find('#id_text')

    def start_new_list(self, item_text):
        self.visit_home()
        input_box = self.get_item_input()
        input_box.send_keys(item_text + '\n')
        list_page = ListPage(self.test)
        list_page.wait_for_new_item_in_list(item_text, 1)
        return list_page


class ListPage(Page):

    def get_list_table_rows(self):
        return self.test.find('#id_list_table tr')

    def wait_for_new_item_in_list(self, item_text, position):
        expected_row = '{}: {}'.format(position, item_text)
        self.test.wait(lambda: self.test.assertIn(
            expected_row,
            [row.text for  row in self.get_list_table_rows()]
        ))

    def get_share_box(self):
        return self.test.find('input[name=email]')

    def get_shared_with_list(self):
        return self.test.find('.list-sharee')

    def share_list_with(self, email):
        self.get_share_box().send_keys(email + '\n')
        self.test.wait(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))
