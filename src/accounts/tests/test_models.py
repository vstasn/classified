from django.test import TestCase
from django.contrib import auth

User = auth.get_user_model()


class UserModelTest(TestCase):
    """test user model"""

    def test_user_is_valid_with_username_and_password_only(self):
        """test: user is valid with username and password only"""
        user = User(username="user1", password="testffd")
        user.full_clean()

    def test_no_problem_with_auth_login(self):
        """test: no problem with auth login"""
        user = User.objects.create(username="user1")
        request = self.client.request().wsgi_request
        auth.login(request, user)
