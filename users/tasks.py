from django.core.mail import EmailMessage
from django.conf import settings
from django.tasks import task
from django.template.loader import get_template

from .models import User
from .utils import (
    get_account_activation_otp_or_url,
    set_cache,
)


@task
def send_account_activation_otp_or_url(user_email: str, send_otp: bool = True):
    try:
        user = User.objects.get(email=user_email)
        otp_or_url = get_account_activation_otp_or_url(
            user=user,
            generate_otp=send_otp,
        )

        html_content = get_template(
            template_name="email/account_activation_email.html",
        ).render(
            context={
                "full_name": user.full_name,
                "email": user_email,
                "otp_or_url": otp_or_url,
                "is_otp": send_otp,
                "timeout": settings.ACCOUNT_ACTIVATION_TOKEN_OR_URL_TIMEOUT,
            },
        )

        email = EmailMessage(
            subject="Account Activation OTP from GreenLeaf",
            body=html_content,
            from_email=None,
            to=[user_email],
        )

        email.content_subtype = "html"
        is_email_send = email.send()
        if is_email_send and send_otp:
            # cache the otp_or_url value if the value is OTP.
            set_cache(
                key=user_email,
                value=otp_or_url,
                timeout=settings.ACCOUNT_ACTIVATION_TOKEN_OR_URL_TIMEOUT,
            )
            return True
        elif is_email_send:
            return True
    except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
        print(e.__class__.__name__, e)
        return False
    except Exception as e:
        print('=======', e)
        return False
    return False
