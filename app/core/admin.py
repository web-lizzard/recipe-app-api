from core import models
from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "name"]


admin.site.register(models.User, UserAdmin)
