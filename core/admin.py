from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _(f"Administration | {settings.SITE_NAME}")
admin.site.site_title = _(f"Site d'administration de {settings.SITE_NAME}")
admin.site.index_title = _(f"Administration | {settings.SITE_NAME}")
