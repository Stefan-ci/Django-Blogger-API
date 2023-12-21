from django.conf import settings
from django.utils.translation import get_language


def global_context(request):
    context = {
        "site_name": settings.SITE_NAME,
        "current_language_code": get_language(),
        "site_email_address": settings.SITE_EMAIL_ADDRESS,
    }
    return context
