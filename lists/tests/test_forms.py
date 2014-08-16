from django.test import TestCase

from ..models import List, Item
from ..forms import (
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
    ItemForm, ExistingListForm
)


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'to-do'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'to-do')
        self.assertEqual(new_item.list, list_)

class ExistingListFormTest(TestCase):

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListForm(for_list=list_, data={'text': 'spam'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='evil twin')
        form = ExistingListForm(for_list=list_, data={'text': 'evil twin'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
