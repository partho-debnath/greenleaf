from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User, CountryCode


class UserModelAdmin(BaseUserAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "mobile_number",
        "created_at",
        "updated_at",
        "is_active",
        "is_superuser",
        "show_image",
    ]
    list_filter = [
        "email",
    ]

    ordering = [
        "email",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "preview_image",
                    "email",
                    "password",
                ]
            },
        ),
        (
            "Personal Information",
            {
                # "classes": [
                #     "collapse"
                # ],  # for show and hide the "Personal info" section
                "fields": [
                    "first_name",
                    "last_name",
                    "address",
                    # "country_code",
                    "mobile_number",
                    "gender",
                    "date_of_birth",
                    "image",
                ],
            },
        ),
        (
            "Permissions",
            {
                "fields": [
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ]
            },
        ),
        (
            "Important Dates",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
        "preview_image",
    ]

    """
    add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    overrides get_fieldsets to use this attribute when creating
    a user using admin panel.
    """
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],  # for css
                "fields": [
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ],
            },
        ),
        (
            "Personal info",
            {
                "classes": ["wide"],  # for css
                "fields": [
                    "address",
                    # "country_code",
                    "mobile_number",
                    "gender",
                    "date_of_birth",
                    "image",
                ],
            },
        ),
        (
            "Permissions",
            {
                "classes": ["collapse"],
                "fields": [
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ],
            },
        ),
    ]
    autocomplete_fields = [
        # "country_code",
    ]

    @admin.display(description="image")
    def preview_image(self, instance):
        if not instance.image:
            return format_html(
                '<img src="" alt="{}" width="20%" />',
                "No Image",
            )
        return format_html(
            '<img src="{}" width="15%" />',
            instance.image.url,
        )


admin.site.register(User, UserModelAdmin)


@admin.register(CountryCode)
class CountryCodeModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code"]
    search_fields = ["name", "code"]
    # list_filter = []
