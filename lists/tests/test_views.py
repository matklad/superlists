import unittest
from unittest.mock import Mock, patch

from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape

from ..views import home_page, new_list
from ..models import Item, List
from ..forms import (
    ItemForm, ExistingListForm,
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
)
User = get_user_model()


class HomePageTest(TestCase):

    def test_home_page_useses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.dtl')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class NewListIntegrationTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_for_invalid_input_doesnt_save_but_shows_errors(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        request = HttpRequest()
        request.user = User.objects.create(email='a@b.com')
        request.POST['text'] = 'foobar'
        new_list(request)
        list_ = List.objects.first()
        self.assertEqual(list_.owner, request.user)



@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, NewListFormMock):
        new_list(self.request)
        NewListFormMock.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_is_valid(self, NewListFormMock):
        mock_form = NewListFormMock.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, NewListFormMock
    ):
        mock_form = NewListFormMock.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(
        self, mock_render, NewListFormMock
    ):
        mock_form = NewListFormMock.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'home.dtl', {'form': mock_form}
        )

    def test_does_not_save_if_form_invalid(self, NewListFormMock):
        mock_form = NewListFormMock.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertFalse(mock_form.save.called)


class ListViewTestCase(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.dtl')

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertIsInstance(response.context['form'], ExistingListForm)
        self.assertContains(response, 'name="text"')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemy 1', list=correct_list)
        Item.objects.create(text='itemy 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other item 1', list=other_list)
        Item.objects.create(text='other item 2', list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response, 'itemy 1')
        self.assertContains(response, 'itemy 2')
        self.assertNotContains(response, 'other item 1')
        self.assertNotContains(response, 'other item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/{}/'.format(list_.id),
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_lists_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.dtl')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListForm)

    def test_for_invalid_input_show_error_on_the_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='quux')
        response = self.client.post(
            '/lists/{}/'.format(list1.id),
            data={'text': 'quux'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.dtl')
        self.assertEqual(Item.objects.count(), 1)


class MyListsTest(TestCase):

    def test_my_lists_view_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.dtl')

    def test_passes_correct_owener_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_owner = User.objects.create(email='correct@owner.com')
        response = self.client.get('/lists/users/correct@owner.com/')
        self.assertEqual(response.context['owner'], correct_owner)
