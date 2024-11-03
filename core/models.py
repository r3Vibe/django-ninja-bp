from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .utils import make_otp_code, make_session_token
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    """
    Custom User Manager

    Creates and saves a User with the given email and password.
    Creates and saves a Admin User with the given email and password.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User Model"""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(unique=True, max_length=255)
    username = None
    password = models.CharField(max_length=256)

    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def get_full_name(self) -> str:
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class EmailsAddress(models.Model):
    """Emails Address Model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emails")
    email = models.EmailField(max_length=255, unique=True)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class SessionTracker(models.Model):
    """Model to track the registration process"""

    STEP_CHOICES = [
        ("register", "Register"),
        ("reset", "Reset Password"),
        ("code_sent", "Code Sent"),
        ("code_verified", "Code Verified"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    session_token = models.CharField(
        max_length=12, unique=True, default=make_session_token
    )
    step = models.CharField(max_length=20, choices=STEP_CHOICES, default="register")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.step})"


class OTPCode(models.Model):
    """Model to track the otp status"""

    session = models.ForeignKey(
        SessionTracker, on_delete=models.CASCADE, related_name="otps"
    )
    code = models.CharField(max_length=6, unique=True, default=make_otp_code)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    otp_sent_at = models.DateTimeField(blank=True, null=True)
    otp_verified_at = models.DateTimeField(blank=True, null=True)

    attempts = models.IntegerField(default=0)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.session.user.get_full_name()} ({self.code})"

    def update_otp_sent_at(self):
        """update the otp sent at time"""
        self.otp_sent_at = timezone.now()
        self.save()

    def update_otp_verified_at(self):
        """update the otp verified at time"""
        self.otp_verified_at = timezone.now()
        self.is_verified = True
        self.save()
