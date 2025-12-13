from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from base.models import TimestampMixin
from users.manager import UserManager


class User(AbstractBaseUser, TimestampMixin, PermissionsMixin):
    """
    User model to store user data and authentication.
    """

    class Gender(models.TextChoices):
        """
        user gender
        """

        MALE = "M", "Male"
        FEMALE = "F", "Female"

    first_name = models.CharField(
        verbose_name="first name",
        max_length=100,
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=100,
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    # country_code = models.ForeignKey(
    #     "CountryCode",
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name="users",
    # )
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
    )
    gender = models.CharField(
        max_length=7,
        choices=Gender.choices,
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(
        help_text="YYYY-MM-DD formate.",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        help_text="Profile picture",
        upload_to="profile_pictures/%Y/%m/%d",
        blank=True,
        null=True,
    )
    address = models.TextField(
        blank=True,
        null=True,
    )

    two_factor_secret_key = models.OneToOneField(
        verbose_name="2FA secret key",
        help_text="""two_factor_secret_key not null
        means 2FA is active for this user.""",
        to="TwoFA",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    is_active = models.BooleanField(
        verbose_name="active",
        db_default=False,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    is_admin = models.BooleanField(
        verbose_name="staff status",
        db_default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name="superuser status",
        db_default=False,
        help_text="Designates that this user has all permissions without "
        "explicitly assigning them.",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["email"]),
        ]

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "date_of_birth",
    ]

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def show_image(self):
        "Show the user profile picture"
        if not self.image:
            return mark_safe("<img src='' alt='No Image' width='25%'/>")
        return mark_safe(
            "<img src='{}' alt='{}' width='25%'/>".format(
                self.image.url, self.image.name
            )
        )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class CountryCode(models.Model):
    """
    store country name and code.
    """

    name = models.CharField(
        max_length=10,
        verbose_name="country name",
    )
    code = models.CharField(
        max_length=10,
        verbose_name="country code",
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["name", "code"],
                name="country_name_code",
            )
        ]
        constraints = [
            models.UniqueConstraint(
                name="unique_country_name_code",
                fields=["name", "code"],
            )
        ]

    def __str__(self):
        return "{},  {}".format(self.name, self.code)


class TwoFA(TimestampMixin):
    """
    store secret-key for two factor authentication using google authenticator.
    """

    secret_key = models.CharField(
        verbose_name="2FA secret key.",
        editable=False,
        db_index=True,
    )

    class Meta:
        verbose_name = "Two Factor Secret Key"
        verbose_name_plural = "Two Factor Secret Key"
