from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

from ..authentication import (
    PERSONA_VERIFY_URL, PersonaAuthenticationBackend
)

@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        User.objects.create(email='otheruser@example.com')

    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('an assertion')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'an assertion', 'audience': settings.DOMAIN}
        )

    def test_returns_none_if_response_errors(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_returns_non_if_not_okay(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'not okay!'}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        mock_post.return_value.json.return_value = {
            'status': 'okay', 'email': 'a@b.com'
        }
        actual_user = User.objects.create(email='a@b.com')

        found_user = self.backend.authenticate('an assertion')
        self.assertEqual(found_user, actual_user)

    def test_crates_user_if_necessary(self, mock_post):
        mock_post.return_value.json.return_value = {
            'status': 'okay', 'email': 'a@b.com'
        }
        found_user = self.backend.authenticate('an assertion')
        new_user = User.objects.get(email='a@b.com')
        self.assertEqual(found_user, new_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='otheruser@example.com')
        desired_user = User.objects.create(email='a@b.com')

        backend = PersonaAuthenticationBackend()
        found_user = backend.get_user('a@b.com')
        self.assertEqual(desired_user, found_user)

    def test_returns_none_if_user_not_found(self):
        backend = PersonaAuthenticationBackend()
        self.assertIsNone(backend.get_user('a@b.com'))
