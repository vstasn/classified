from django.test import TestCase
from unittest.mock import patch, call


class SignUpTest(TestCase):
    """test view for sign up"""

    def test_redirects_to_home_page(self):
        """test: redirects to home page"""
        response = self.client.post(
            "/accounts/register",
            data={
                "username": "user1",
                "password1": "test1234#",
                "password2": "test1234#",
            },
        )
        self.assertRedirects(response, "/")

    def test_adds_success_message(self):
        """test: adds success message"""
        response = self.client.post(
            "/accounts/register",
            data={
                "username": "user1",
                "password1": "test1234#",
                "password2": "test1234#",
            },
            follow=True,
        )

        message = list(response.context["messages"])[0]
        self.assertEqual(message.message, "User created, sign in, please")
        self.assertEqual(message.tags, "success")

    @patch("accounts.views.messages")
    def test_adds_success_message_with_mocks(self, mock_messages):
        """test: adds success message with mock"""
        response = self.client.post(
            "/accounts/register",
            data={
                "username": "user1",
                "password1": "test1234#",
                "password2": "test1234#",
            },
        )

        expected = "User created, sign in, please"
        self.assertEqual(
            mock_messages.success.call_args, call(response.wsgi_request, expected)
        )


@patch("accounts.views.auth")
class LoginViewTest(TestCase):
    """login view test"""

    def test_redirects_to_home_page(self, mock_auth):
        """test: redirects to home page"""
        response = self.client.post("/accounts/login")
        self.assertRedirects(response, "/")

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        """test: calls auth login with user if there is one"""
        response = self.client.post(
            "/accounts/login", data={"username": "user1", "password1": "test1234#"}
        )
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value),
        )
