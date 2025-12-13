import secrets
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse
from django.utils.http import base36_to_int
from django.utils.crypto import constant_time_compare
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)


class AccountActiveTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        value = super()._make_hash_value(user=user, timestamp=timestamp)
        return f"{value}{user.is_active}"

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        for secret in [self.secret, *self.secret_fallbacks]:
            if constant_time_compare(
                self._make_token_with_timestamp(user, ts, secret),
                token,
            ):
                break
        else:
            return False

        # Check the timestamp is within limit.
        if (
            self._num_seconds(self._now()) - ts
        ) > settings.ACCOUNT_ACTIVATION_TOKEN_OR_URL_TIMEOUT:
            return False

        return True


def get_account_activation_otp_or_url(user, generate_otp: bool = True) -> str:
    """
    generate account activation OTP or URL based on the user.
    """
    if generate_otp:
        return str(get_secret_otp())
    else:
        return get_account_activation_url(user=user)


def get_secret_otp() -> int:
    return secrets.randbits(20)


def get_urlsafe_encoded_data(data) -> str:
    return urlsafe_base64_encode(force_bytes(data))


def get_urlsafe_decoded_data(encoded_data) -> str:
    if isinstance(encoded_data, (str, bytes)) is False:
        encoded_data = str(encoded_data)
    return urlsafe_base64_decode(encoded_data).decode("utf-8")


def get_account_activation_url(user) -> str:
    """
    generate account activation url
    """

    encoded_uid = get_urlsafe_encoded_data(data=user.id)
    token = AccountActiveTokenGenerator().make_token(user=user)

    path = reverse(
        viewname="users:activate_account",
        kwargs={
            "token": token,
            "uid": encoded_uid,
        },
    )
    return f"{settings.SITE_SCHEME}://{settings.SITE_DOMAIN}{path}"


def set_cache(key: str, value: str, timeout: int = 60):
    """
    cache data with key value for a specific time in sec.
    """
    cache.set(key=key, value=value, timeout=timeout)


def verify_otp(email: str, otp: str) -> bool:
    """Check if OTP for given email matches cache."""
    cached_otp = cache.get(key=email, default=None)
    return cached_otp == otp
