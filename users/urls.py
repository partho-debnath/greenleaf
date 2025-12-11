from django.urls import path

from .views import (
    UserLoginView,
)

app_name = "users"
urlpatterns = [
    path(route="login/", view=UserLoginView.as_view(), name="user_login"),
]
