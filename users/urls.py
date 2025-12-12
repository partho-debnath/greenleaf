from django.urls import path

from .views import (
    UserLoginView,
    UserRegistrationView,
)

app_name = "users"
urlpatterns = [
    path(route="login/", view=UserLoginView.as_view(), name="user_login"),
    path(
        route="registration/",
        view=UserRegistrationView.as_view(),
        name="user_registration",
    ),
]
