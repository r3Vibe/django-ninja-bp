from django.utils.crypto import get_random_string


def make_session_token():
    """Generate a new session token (12 characters)"""
    return get_random_string(12)


def make_otp_code():
    """Generate a new OTP code (6 characters)"""
    return get_random_string(6)
