from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, HASH_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    '''command'''

    def add_arguments(self, parser):
        '''add arguments'''
        parser.add_argument('username')

    def handle(self, *args, **options):
        '''handle'''
        session_key = create_pre_authenticated_session(options['username'])
        self.stdout.write(session_key)


def create_pre_authenticated_session(username):
    '''create pre authenticated session'''
    user = User.objects.create(username=username)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session.session_key
