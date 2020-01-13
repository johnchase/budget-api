from .base import *  # noqa: F403, F401

ALLOWED_HOSTS = ['api.johnhchase.com']

DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
        "https://budgetx.johnhchase.com"
)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
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
