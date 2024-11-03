from config.env import env

CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = env.bool("DJANGO_CORS_ALLOW_CREDENTIALS", default=False)
