from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView

from users.models import User
from users.utils import AccountActiveTokenGenerator, get_urlsafe_decoded_data

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


class AccountActivationView(RedirectView):

    http_method_names = ("get",)

    def get(self, request, *args, **kwargs):
        try:
            urlsafe_encoded_uid = kwargs.get("uid")
            user_id = get_urlsafe_decoded_data(
                encoded_data=urlsafe_encoded_uid,
            )
            user = User.objects.get(id=int(user_id))
            is_valid_token = AccountActiveTokenGenerator().check_token(
                user=user,
                token=kwargs.get("token"),
            )
            if is_valid_token is True:
                user.is_active = True
                user.save()
                messages.success(
                    request=request,
                    message="Account activation Success. Now you can login.",
                )
            else:
                messages.error(
                    request=request,
                    message="Account activation failed.",
                )
        except (User.DoesNotExist, Exception):
            messages.error(
                request=request,
                message="Account activation failed.",
            )
        return redirect("users:user_login")
