from accounts.models import User
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin



class CustomGroupAdmin(GroupAdmin):
    def has_delete_permission(self, request, obj=None):
        return False



class CustomUserAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    list_display = ["email", "username", "phone_number", "gender", "is_active", "is_staff", "is_superuser", "date_joined"]
    search_fields = ["email", "username", "phone_number", "is_active", "is_staff", "is_superuser", "date_joined",
        "first_name", "last_name", "last_login", "zip_code", "country", "account_confirmed", "gender", "address", "city"]
    list_filter = ["account_confirmed", "is_active", "is_staff", "is_superuser", "gender", "date_joined"]
    filter_horizontal = ["groups", "user_permissions"]
    date_hierarchy = "date_joined"
    
    summernote_fields = ["bio"]
    
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    # def has_change_permission(self, request, obj=None):
    #     return False
    
    
    fieldsets = [
        (_("Informations personnelles"), {
            "fields": ["username", "first_name", "last_name", "email", "phone_number", "gender"]
        }),
        
        (_("Dates importantes"), {
            "fields": ["date_joined", "last_login"]
        }),
        
        (_("Status"), {
            "fields": ["is_active", "is_staff", "is_superuser", "account_confirmed"]
        }),
        
        (_("Pays & Adresses"), {
            "fields": ["country", "region", "city", "zip_code", "address"]
        }),
        
        (_("Profil"), {
            "fields": ["avatar", "website", "bio"]
        }),
        
        (_("Groupes"), {
            "fields": ["groups"]
        }),
        
        (_("Permissions"), {
            "fields": ["user_permissions"]
        }),
        
        (_("Métadonnées"), {
            "fields": ["uuid", "extra_data"]
        }),
    ]




admin.site.unregister(Group) # Unregister it first and register again with "CustomGroupAdmin"

admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
