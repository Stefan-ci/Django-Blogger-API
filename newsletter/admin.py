from django.contrib import admin
from newsletter.models import Newsletter
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

class NewsletterAdmin(ImportExportModelAdmin):
    list_display = ["email", "is_subscribed", "is_deleted", "date"]
    list_filter = ["date", "is_subscribed", "is_deleted"]
    search_fields = ["email"]
    date_hierarchy = "date"

admin.site.register(Newsletter, NewsletterAdmin)
