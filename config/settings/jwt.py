from datetime import timedelta
from config.env import env

NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS512",
    "SIGNING_KEY": env("JWT_SECRET_KEY"),
    "VERIFYING_KEY": None,
    "AUDIENCE": "app",
    "ISSUER": "boilerplate",
    "JWK_URL": None,
    "LEEWAY": 0,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user",
    "USER_AUTHENTICATION_RULE": "ninja_jwt.authentication.default_user_authentication_rule",
}


"""
clear the expired tokens form db

python manage.py flushexpiredtokens

"""
