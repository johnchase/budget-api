from .base import *  # noqa: F403, F401

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ORIGIN_WHITELIST = ("http://127.0.0.1:4200", "http://localhost:4200")
