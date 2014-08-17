from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from ..models import Item, List
User = get_user_model()


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_)
        self.assertIn(item, list_.item_set.all())

    def test_items_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='i1')
        item2 = Item.objects.create(list=list_, text='item 2')
        item3 = Item.objects.create(list=list_, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_cannot_save_empty_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_cannot_save_duplicate_item(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='foo')

        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='foo')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='bar')

        item2 = Item(list=list2, text='bar')
        item2.full_clean()

    def test_item_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(
            list_.get_absolute_url(),
            '/lists/{}/'.format(list_.id)
        )

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_create_new_returns_new_list_object(self):
        user = User.objects.create()
        ret = List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(ret, new_list)

    def test_lists_can_have_owners(self):
        List(owner=User())

    def test_lis_owner_is_optional(self):
        List().full_clean()

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        list_.item_set.create(text='first')
        list_.item_set.create(text='second')
        self.assertEqual(list_.name, 'first')
