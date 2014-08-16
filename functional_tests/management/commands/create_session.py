from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import get_user_model, BACKEND_SESSION_KEY, SESSION_KEY
User = get_user_model()


class Command(BaseCommand):

    def handle(self, email, *_, **__):
        session_key = create_pre_authenticated_session(email)
        self.stdout.write(session_key)


def create_pre_authenticated_session(email):
    user = User.objects.create(email=email)

    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
