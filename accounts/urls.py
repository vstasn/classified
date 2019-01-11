from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^login$", views.login_view, name="login"),
    url(r"^register$", views.UserCreate.as_view(), name="register"),
    url(r"^logout$", views.LogoutView.as_view(next_page="/"), name="logout"),
]
