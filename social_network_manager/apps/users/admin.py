from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User, UserNetwork, FriendRequest


class CustomUserAdmin(UserAdmin):
    """
    Custom Admin to replace signup via email and not username from admin.
    """
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined", "created_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(FriendRequest)
admin.site.register(UserNetwork)
