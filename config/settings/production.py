from .base import *  # noqa: F403, F401

ALLOWED_HOSTS = ["api.johnhchase.com"]

DEBUG = False
#SECURE_SSL_REDIRECT = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ("https://budget.johnhchase.com",)
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    "Access-Control-Allow-Origin",
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)
