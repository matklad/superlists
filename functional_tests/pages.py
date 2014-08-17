class Page(object):

    def __init__(self, test):
        self.test = test

    def get_item_input(self):
        return self.test.find('#id_text')


class HomePage(Page):

    def visit_home(self):
        self.test.browser.get(self.test.server_url)
        self.test.wait(self.get_item_input)
        return self

    def visit_my_lists(self):
        self.test.browser.find_element_by_link_text('My lists').click()
        self.test.wait_for(lambda: self.test.assertEqual(
            self.test.find('h1').text,
            'My Lists'
        ))

    def start_new_list(self, item_text):
        self.visit_home()
        input_box = self.get_item_input()
        input_box.send_keys(item_text + '\n')
        list_page = ListPage(self.test)
        list_page.wait_for_new_item_in_list(item_text, 1)
        return list_page


class ListPage(Page):

    def get_list_table_rows(self):
        return self.test.find_all('#id_list_table tr')

    def wait_for_new_item_in_list(self, item_text, position):
        expected_row = '{}: {}'.format(position, item_text)
        self.test.wait(lambda: self.test.assertIn(
            expected_row,
            [row.text for  row in self.get_list_table_rows()]
        ))

    def get_share_box(self):
        return self.test.find('input[name=email]')

    def get_shared_with_list(self):
        return self.test.find_all('.list-sharee')

    def share_list_with(self, email):
        self.get_share_box().send_keys(email + '\n')
        self.test.wait(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))

    def add_new_item(self, item_text):
        current_pos = len(self.get_list_table_rows())
        self.get_item_input().send_keys(item_text + '\n')
        self.wait_for_new_item_in_list(item_text, current_pos + 1)

    def get_list_owner(self):
        return self.test.find('#id_list_owner').text
