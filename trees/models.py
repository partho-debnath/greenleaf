from math import ceil
from django.db import models
from django.utils.text import slugify

from base.models import TimestampMixin


class Category(TimestampMixin):
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
        db_index=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sub_categories",
    )
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "parent_category"],
                name="unique_category",
            ),
        ]

    def __str__(self):
        return self.name


class Product(TimestampMixin):
    name = models.CharField(
        max_length=200,
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name="products",
        db_index=True,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_index=True,
    )
    stock = models.PositiveIntegerField(
        default=0,
    )
    thumbnail = models.ImageField(
        upload_to="products/thumbnails/",
        blank=True,
        null=True,
    )
    scientific_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    growth_time = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    care_instructions = models.TextField(
        blank=True,
        null=True,
    )

    height_cm = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    seed_weight_grams = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    is_available = models.BooleanField(
        default=True,
    )
    rating_sum = models.PositiveIntegerField(default=0)
    rating_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def average_rating(self) -> int:
        if self.rating_count > 0:
            return ceil(self.rating_sum / self.rating_count)
        else:
            return 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name} {self.category.name}")
        super().save(*args, **kwargs)


class ProductSpecification(TimestampMixin):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="specifications",
        db_index=True,
    )
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    sort_order = models.IntegerField()
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "key"],
                name="unique_specification",
            )
        ]
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.key}: {self.value}"


class ProductImage(TimestampMixin):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        upload_to="products/images/",
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    sort_order = models.IntegerField()
    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f"Image of {self.product.name}"

    class Meta:
        ordering = ["sort_order", "id"]
