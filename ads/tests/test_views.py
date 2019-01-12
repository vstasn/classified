from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from ads.models import Ads, AdsCity
import fakeredis


User = get_user_model()


def create_ads(title, description):
    user = User.objects.create()
    city = AdsCity.objects.create()
    return Ads.objects.create(
        title=title, description=description, owner=user, city=city
    )


class AdsViewTest(TestCase):
    def test_no_classified_ads(self):
        """
        If no ads exist, an appropriate message is displayed.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no ads in the classified.")

    def test_classified_ads(self):
        """
        Ads are displayed on the index page.
        """
        create_ads(title="Title2", description="Desc2")
        response = self.client.get("/")
        self.assertQuerysetEqual(response.context["ads_list"], ["<Ads: Title2>"])

    @patch("ads.counter.connect", fakeredis.FakeRedis(db=0))
    def test_classified_ads_page_hit(self):
        """
        Ads are displayed on detail page and page hit counter is working
        """
        ads_ = create_ads(title="Title2", description="Desc2")
        response = self.client.get(f"/ads/{ads_.id}/")
        self.assertEqual(response.context["view_count"], 1)

    @patch("ads.counter.connect", fakeredis.FakeRedis(db=1))
    def test_classified_ads_page_hit_twice(self):
        """
        Ads are displayed on detail page and page hit counter is working
        """
        ads_ = create_ads(title="Title2", description="Desc2")
        # open twice, should increment just one
        response1 = self.client.get(f"/ads/{ads_.id}/")
        response2 = self.client.get(f"/ads/{ads_.id}/")
        self.assertEqual(response2.context["view_count"], 1)
        self.assertEqual(
            response1.context["view_count"], response2.context["view_count"]
        )
