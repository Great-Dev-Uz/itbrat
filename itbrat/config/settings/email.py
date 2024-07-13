from config.settings.base import *

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "istamovibrohim8@gmail.com"
EMAIL_HOST_PASSWORD = "xuaokkmfmsaxbdyu"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 300
DEFAULT_FROM_EMAIL = "unipointsoftwaredevelopment@gmail.com"