# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ["email", "is_admin"]
    search_fields = ["email"]


admin.site.register(CustomUser, CustomUserAdmin)
