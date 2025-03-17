from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "date_of_birth", "joined_date", "last_activity")
    ordering = ("joined_date",)
    search_fields = ('username', 'email')

    # Define the structure of fields in the form when creating or editing a user
    fieldsets = (
        (None, {"fields": ("username", "email")}),
        ("Personal Info", {"fields": ("bio", "website", "date_of_birth", "social_links")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "joined_date", "last_activity")}),
    )

    # Modify the fieldsets based on user permissions
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # If the current user is not a superuser, remove the "Permissions" section from the form
        if not request.user.is_superuser:
            fieldsets = [
                fs for fs in fieldsets if fs[0] != "Permissions"
            ]
        return fieldsets

    # Filter the queryset of users based on the current user's permissions
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    # Allow deletion only if the user is a superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
