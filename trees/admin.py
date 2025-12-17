from django.contrib import admin

from .models import (
    Category,
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
        "name", "category", "price", "stock",
        "scientific_name", "growth_time", "is_available"
    ]
    list_filter = [
        "category",
    ]
    search_fields = [
        "name", "category", "description",
        "scientific_name",
    ]
