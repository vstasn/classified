from django.conf.urls import url
from . import views
from .admin import admin_site

urlpatterns = [
    url(r"^(?P<pk>\d+)$", views.AdsDetailView.as_view(), name="ads-detail"),
    url(r"^myads/", admin_site.urls, name="mydetail"),
]
