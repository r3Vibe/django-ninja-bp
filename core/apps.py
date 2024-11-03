from django.apps import AppConfig
from django.db.models.signals import post_save
from .signals import post_save_user, post_save_emails, send_verification_emails


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self) -> None:
        post_save.connect(post_save_user, sender=self.get_model("User"))
        post_save.connect(post_save_emails, sender=self.get_model("EmailsAddress"))
        post_save.connect(send_verification_emails, sender=self.get_model("OTPCode"))
