from django.urls import path

from .views import (
    AccountActivationView,
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
    path(
        route="<str:token>/<str:uid>/active-account/",
        view=AccountActivationView.as_view(),
        name="activate_account",
    )
]
