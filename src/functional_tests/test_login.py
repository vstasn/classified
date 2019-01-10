from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LoginTest(FunctionalTest):
    def test_can_sign_up_with_username(self):
        """register user"""
        test_user = "user1"
        test_pass = "test1234#"

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("signup").click()

        self.wait_for(
            lambda: self.assertIn(
                "Sign up", self.browser.find_element_by_tag_name("h2").text
            )
        )

        self.browser.find_element_by_name("username").send_keys(test_user)
        self.browser.find_element_by_name("password1").send_keys(test_pass)
        self.browser.find_element_by_name("password2").send_keys(test_pass)
        self.browser.find_element_by_name("username").send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertIn(
                "User created", self.browser.find_element_by_tag_name("body").text
            )
        )

        # try to log in with created user
        self.browser.find_element_by_name("username").send_keys(test_user)
        self.browser.find_element_by_name("password").send_keys(test_pass)
        self.browser.find_element_by_name("username").send_keys(Keys.ENTER)

        self.wait_to_be_logged_in(username=test_user)

        self.browser.find_element_by_link_text("Log out").click()

        self.wait_to_be_logged_out(username=test_user)
