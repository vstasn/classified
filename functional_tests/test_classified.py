from .base import FunctionalTest
from selenium.webdriver.support.select import Select


class ClassifiedTest(FunctionalTest):
    """test classified ads"""

    def test_create_new_classified_ads(self):
        self.create_pre_authenticated_session("user31", "test1234#")

        self.browser.refresh()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text("Add ads").click()

        # create new classified ads
        self.browser.find_element_by_name("title").send_keys("Title1")
        self.browser.find_element_by_name("description").send_keys("Desc1")
        select = Select(self.browser.find_element_by_name("city"))
        select.select_by_index(1)
        self.browser.find_element_by_name("_save").click()

        # should not raise
        self.browser.find_elements_by_link_text("Title1")
