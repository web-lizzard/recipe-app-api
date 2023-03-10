from core import models
from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as translate


# Register your models here.
class UserAdmin(BaseUserAdmin):
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
