from django.contrib import admin
from blog.models import Post, Category, Comment
from import_export.admin import ImportExportModelAdmin
from django_summernote.admin import SummernoteModelAdmin


class CategoryAdmin(ImportExportModelAdmin):
    list_display = ["name", "is_active", "date"]
    list_filter = ["is_active", "date"]
    search_fields = ["name", "slug", "is_active", "date", "updated_on"]
    date_hierarchy = "date"
    
    def has_delete_permission(self, request, obj=None):
        return False


class PostAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    list_display = ["title", "category", "author", "is_public", "date"]
    list_filter = ["category", "is_public", "date"]
    search_fields = ["title", "category__name", "category__slug", "author__email", "author__username", "author__first_name",
        "author__lastname", "description", "summary", "tags", "uuid", "is_public", "date", "updated_on"]
    date_hierarchy = "date"
    
    summernote_fields = ["bio"]
    
    
    def has_delete_permission(self, request, obj=None):
        return False




class CommentAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    list_display = ["post", "user", "is_public", "date"]
    list_filter = ["is_public", "date"]
    search_fields = ["post__title", "post__category__name", "post__category__slug", "post__author__email",
        "post__author__username", "post__author__first_name", "post__author__lastname", "post__description", "post__summary",
        "post__tags", "post__uuid", "post__is_public", "post__date", "post__updated_on", "comment", "uuid", "is_public", "date",
        "updated_on"]
    date_hierarchy = "date"
    
    summernote_fields = ["comment"]
    
    
    def has_delete_permission(self, request, obj=None):
        return False





admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
