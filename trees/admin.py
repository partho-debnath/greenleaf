from django.contrib import admin

from .models import (
    Category,
    Discount,
    Product,
    ProductSpecification,
    ProductImage,
)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = [
        "name", "description", "parent_category", "is_active",
    ]
    list_filter = [
        "parent_category",
        "is_active",
    ]
    search_fields = [
        "name", "description", "parent_category",
    ]


@admin.register(Discount)
class DiscountModelAdmin(admin.ModelAdmin):
    list_display = (
        "name", "discount_type", "value", "is_active", "created_at",
    )
    search_fields = ("name", )


class ProductSpecificationModelAdminInline(admin.TabularInline):
    model = ProductSpecification
    extra = 5


class ProductImageInlineModelAdmin(admin.TabularInline):
    model = ProductImage
    extra = 4


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationModelAdminInline,
        ProductImageInlineModelAdmin,
    ]
    list_display = [
        "name", "category", "price", "stock", "discount",
        "scientific_name", "growth_time", "is_available"
    ]
    list_filter = [
        "category", "discount",
    ]
    search_fields = [
        "name", "category", "description",
        "scientific_name",
    ]
    autocomplete_fields = ("discount",)
