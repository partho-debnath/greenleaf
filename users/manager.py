from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(
        self,
        first_name,
        last_name,
        email,
        date_of_birth=None,
        password=None,
    ):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not first_name:
            raise ValueError("User must have an first name")
        elif not last_name:
            raise ValueError("User must have an last name")
        elif not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, first_name, last_name, email, date_of_birth, password=None
    ):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
