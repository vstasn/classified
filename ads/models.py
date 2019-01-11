from django.db import models
from django.conf import settings
from django.urls import reverse


class AdsCity(models.Model):
    """
    Store cities
    """
    city = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.city


class Ads(models.Model):
    """
    Classified ads
    """
    title = models.TextField()
    description = models.TextField()
    city = models.ForeignKey(AdsCity, blank=False, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("ads-detail", args=[self.id])
