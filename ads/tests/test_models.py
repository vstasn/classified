from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from ads.models import Ads, AdsCity

User = get_user_model()


class CityModelTest(TestCase):
    """test: ads city model"""

    def test_create_city_without_name(self):
        city = AdsCity.objects.create()
        # should raise
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_create_city_valid(self):
        city = AdsCity.objects.create(city="Moscow")
        city2 = AdsCity.objects.first()

        self.assertEqual(city.city, city2.city)


class AdsModelTest(TestCase):
    """test: ads model"""

    def test_get_absolute_url(self):
        """test: get absolute url"""
        user = User.objects.create()
        city = AdsCity.objects.create()
        ads_ = Ads.objects.create(owner=user, city=city)
        self.assertEqual(ads_.get_absolute_url(), f"/ads/{ads_.id}/")

    def test_create_new_without_city(self):
        user = User.objects.create()
        # should raise
        with self.assertRaises(IntegrityError):
            ads_ = Ads.objects.create(owner=user)
            ads_.full_clean()

    def test_create_new_without_user(self):
        city = AdsCity.objects.create()
        # should raise
        with self.assertRaises(IntegrityError):
            ads_ = Ads.objects.create(city=city)
            ads_.full_clean()

    def test_create_new_can_check_saved(self):
        user = User.objects.create()
        city = AdsCity.objects.create()
        ads_ = Ads.objects.create(
            title="test2", description="desc2", owner=user, city=city
        )

        self.assertEqual(ads_.title, "test2")
        self.assertEqual(ads_.description, "desc2")
