from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password", "is_supervisor")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_supervisor",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
