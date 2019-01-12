from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from .management.commands.create_session import create_pre_authenticated_session
from ads.models import AdsCity
import time


MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """functional test"""

    def setUp(self):
        """install"""
        self.browser = webdriver.Firefox()
        self.create_catalog_cities()

    def tearDown(self):
        """uninstall"""
        self.browser.quit()
        super().tearDown()

    @wait
    def wait_for(self, fn):
        """wait"""
        return fn()

    @wait
    def wait_to_be_logged_in(self, username):
        """wait to be logged in"""
        self.browser.find_element_by_link_text("Log out")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(username, navbar.text)

    @wait
    def wait_to_be_logged_out(self, username):
        """wait to be logged out"""
        self.wait_for(lambda: self.browser.find_element_by_name("username"))
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(username, navbar.text)

    def create_pre_authenticated_session(self, username):
        """create pre authenticated session"""
        session_key = create_pre_authenticated_session(username)

        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path="/",
                secure=False,
            )
        )

    def create_catalog_cities(self):
        """create catalog cities"""
        city1 = AdsCity.objects.create(city="Moscow")
        city2 = AdsCity.objects.create(city="Perm")
        self.cities = [city1, city2]
