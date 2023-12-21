from django.contrib import admin
from contact.models import Contact
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin

class ContactAdmin(ImportExportModelAdmin):
    list_display = ["subject", "email", "phone_number", "name", "is_answered", "date"]
    list_filter = ["date", "is_answered"]
    search_fields = ["subject", "email", "phone_number", "name", "is_answered", "date", "message"]
    date_hierarchy = "date"
    
    summernote_fields = ["message"]
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Contact, ContactAdmin)
