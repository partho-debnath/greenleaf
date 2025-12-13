from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from base.forms import PHONE_NUMBER_CSS_CLASS, BaseForm, BaseModelForm
from users.models import User


class UserCreationForm(BaseModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password = forms.CharField(
        max_length=30,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
            }
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            # "country_code",
            "mobile_number",
            "image",
            "password",
        ]
        labels = {
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "mobile_number": "Phone Number",
            "image": "Profile Picture",
        }
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                }
            ),
            "mobile_number": forms.TextInput(
                attrs={
                    "class": PHONE_NUMBER_CSS_CLASS,
                    "placeholder": "+88015XXXXXXXX",
                },
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "hidden",
                    "id": "image-input",
                    "onchange": "showImage(event)",
                }
            )
        }

    def clean_confirm_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="../password/">This form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "date_of_birth",
            "is_active",
            "is_admin",
        ]


class UserLoginForm(BaseForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
            }
        )
    )
    password = forms.CharField(
        max_length=30,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
            }
        ),
    )
