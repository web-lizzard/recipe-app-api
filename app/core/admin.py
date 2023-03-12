from core import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as translate


class UserAdmin(BaseUserAdmin):
    """Class to customize admin panel for user entities"""

    ordering = ["email"]
    list_display = ["email", "name", "id"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            translate("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (translate("Important dates"), {"fields": ("last_login",)}),
    )

    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
