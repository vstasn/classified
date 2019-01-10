from django.db import models
from django.conf import settings


class AdsCity(models.Model):
    city = models.TextField(blank=False, null=False)


class Ads(models.Model):

    title = models.TextField()
    description = models.TextField()
    city = models.ForeignKey(
        AdsCity, blank=False, null=False, on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE
    )
