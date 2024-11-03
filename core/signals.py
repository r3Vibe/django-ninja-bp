def post_save_emails(sender, instance, created, **kwargs):
    """
    New Email added then we will have to link the primary email to the user
    check for the is_verified field for email verfications
    """

    if created and instance.is_primary:
        """ It is a new entry with primary true """
        from django.contrib.auth import get_user_model
        from .models import EmailsAddress

        user = get_user_model()
        this_user = user.objects.get(id=instance.user.id)

        this_user.email = instance.email
        this_user.save()

        all_emails_of_this_user = EmailsAddress.objects.filter(user=this_user).exclude(
            id=instance.id
        )

        for email in all_emails_of_this_user:
            email.is_primary = False
            email.save()


def post_save_user(sender, instance, created, **kwargs):
    """
    sender will always be User model
    instance will be the user instance with all the data
    created is True for registration and False for update

    Task is to manage the Email Addresses and Sending Verification Emails
    """

    from .models import EmailsAddress

    if created:
        """  Create Email Addresses for new registrations  """
        EmailsAddress.objects.create(
            user=instance, email=instance.email, is_primary=True
        )

    else:
        """ when user is modified and email was updated """
        if EmailsAddress.objects.filter(email=instance.email, user=instance).exists():
            email_address = EmailsAddress.objects.get(
                email=instance.email, user=instance
            )
            email_address.is_primary = True
            email_address.save()
        else:
            EmailsAddress.objects.create(user=instance, email=instance.email)


def send_verification_emails(sender, instance, created, **kwargs):
    if created:
        from django.core.mail import send_mail

        try:
            """ send verification emails """
            send_mail(
                subject="Verify Your Email Address",
                html_message=f"""
                    <p>Hi {instance.session.user.get_full_name()}</p>
                    <p>Thank you for registering with us. Please verify your email address with the code below</p>
                    <p>{instance.code}</p>
                    <p>If you did not register with us, please ignore this email</p>
                    """,
                fail_silently=False,
                recipient_list=[instance.session.user.email],
                from_email=None,
                message="",
            )
        except Exception as e:
            print(e)
