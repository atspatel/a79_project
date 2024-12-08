# accounts/urls.py

from django.urls import path
from .views import LoginView, UserView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/", UserView.as_view(), name="get_user_email"),
]
