from .base import *  # noqa: F403, F401
import requests

ALLOWED_HOSTS = ["api.johnhchase.com"]

DEBUG = False

EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4", timeout=0.01).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

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
