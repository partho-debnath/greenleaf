from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from base.models import TimestampMixin
from trees.models import Product
from users.models import User


class UserReview(TimestampMixin):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="user_reviews",
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="product_reviews",
        db_index=True,
    )
    review = models.TextField(
        blank=False,
        null=False,
    )


class UserRating(TimestampMixin):
    class RattingChoice(models.IntegerChoices):
        ONE = 1, '1'
        TWO = 2, '2'
        THREE = 3, '3'
        FOUR = 4, '4'
        FIVE = 5, '5'

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="user_ratings",
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="product_ratings",
    )
    rating = models.IntegerField(
        choices=RattingChoice.choices,
        validators=[
            MinValueValidator(limit_value=RattingChoice.ONE.value),
            MaxValueValidator(limit_value=RattingChoice.FIVE.value),
        ],
    )

    class Meta:
        constraints = [
           models.UniqueConstraint(
               fields=["user", "product"],
               name="unique_rating",
           ),
        ]
        indexes = [
            models.Index(fields=["user", "product"],),
        ]
