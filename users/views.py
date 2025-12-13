from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.models import User

from .forms import (
    UserCreationForm,
    UserLoginForm,
)


class UserLoginView(View):
    template_name = "login.html"
    user_login_form = UserLoginForm

    def get(self, request):
        return render(
            request=request,
            template_name=self.template_name,
            context={
                "login_form": self.user_login_form()
            }
        )

    def post(self, request):
        form = self.user_login_form(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        return render(
            request=request,
            template_name=self.template_name,
            context={
                "login_form": form,
            }
        )


class UserRegistrationView(SuccessMessageMixin, CreateView):
    template_name = "registration.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("users:user_login")
    success_message = "Account created successfully. Check your email to activate your account."
