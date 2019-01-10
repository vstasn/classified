from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    url(r'^login$', views.login_view, name='login'),
    url(r'^register$', views.UserCreate.as_view(), name='register'),
    url(r'^logout$', LogoutView.as_view(template_name="base.html"), name='logout'),
]
