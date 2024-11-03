from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.http import HttpRequest
from .models import EmailsAddress, SessionTracker, OTPCode
from typing import Any


from unfold.admin import ModelAdmin, TabularInline


from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group


admin.site.unregister(Group)


class UserEmails(TabularInline):
    model = EmailsAddress
    extra = 0
    readonly_fields = ("is_primary", "is_verified")
    fields = ("email", "is_primary", "is_verified")

    def has_add_permission(self, request: HttpRequest, obj):
        return False


@admin.register(get_user_model())
class UserAdmin(UserAdmin, ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    ordering = ("email",)
    list_editable = ("is_active", "is_staff", "is_superuser")
    list_display_links = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    inlines = (UserEmails,)

    fieldsets = (
        (
            "General Info",
            {
                "fields": ("first_name", "last_name", "password"),
            },
        ),
        (
            "Contact Info",
            {
                "fields": ("email",),
            },
        ),
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
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            "General Info",
            {
                "fields": ("first_name", "last_name", "password1", "password2"),
            },
        ),
        (
            "Contact Info",
            {
                "fields": ("email",),
            },
        ),
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
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )


@admin.register(EmailsAddress)
class EmailsAddressAdmin(ModelAdmin):
    list_display = ("email", "is_primary", "is_verified", "created_at", "updated_at")
    ordering = ("email",)
    list_editable = ("is_primary", "is_verified")
    list_display_links = ("email",)
    list_filter = ("is_primary", "is_verified", "user")

    def save_model(
        self, request: HttpRequest, obj: Any, form: ModelForm, change: bool
    ) -> None:
        if obj.is_primary:
            EmailsAddress.objects.filter(user=obj.user).exclude(id=obj.id).update(
                is_primary=False
            )
            get_user_model().objects.filter(id=obj.user.id).update(email=obj.email)
        else:
            any_primary = (
                EmailsAddress.objects.filter(user=obj.user, is_primary=True)
                .exclude(id=obj.id)
                .exists()
            )
            if not any_primary:
                self.message_user(
                    request, "Atleast one primary email is required", level="error"
                )
                return
        return super().save_model(request, obj, form, change)


@admin.register(SessionTracker)
class SessionTrackerAdmin(ModelAdmin):
    list_display = ("user", "step", "created_at", "updated_at")
    ordering = ("user",)
    list_display_links = ("user",)
    list_filter = ("step",)


@admin.register(OTPCode)
class OTPCodeAdmin(ModelAdmin):
    list_display = (
        "session",
        "code",
        "attempts",
        "is_verified",
        "created_at",
        "updated_at",
    )
    ordering = ("session",)
    list_display_links = ("session",)
    list_filter = ("session",)
    readonly_fields = ("otp_sent_at", "otp_verified_at", "is_verified")


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
