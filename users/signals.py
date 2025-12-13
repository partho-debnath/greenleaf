from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .tasks import send_account_activation_otp_or_url


@receiver(signal=post_save, sender=User)
def user_change(sender, instance: User, created: bool, *args, **kwargs):
    if created:
        send_account_activation_otp_or_url.enqueue(
            instance.email,
            False,
        )
