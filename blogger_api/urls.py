from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.static import serve
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


BASE_URL = "api"
VERSION_1_BASE_URL = "v1"


urlpatterns = [
    # INTERNATIONALIZATION
    path("i18n/", include("django.conf.urls.i18n")),
    
    # 3rd party apps URLs
    path("summernote/", include("django_summernote.urls")),
    path("rest/framework/", include("rest_framework.urls")),
    
    # Locale API apps URLs
    path(f"{BASE_URL}/{VERSION_1_BASE_URL}/", include("blogger_api.v1_urls", namespace="api-v1")), # v1 base URLs entry point
]

# Translated URLs
urlpatterns += i18n_patterns(
    # Django admin
    path(f"{settings.DJANGO_ADMIN_PAGE_URL}/admindocs/", include("django.contrib.admindocs.urls")), # Must appear before admin.site.urls
    path(f"{settings.DJANGO_ADMIN_PAGE_URL}/", admin.site.urls),
    
    # Locale templates apps URLs
    path("", include("core.urls", namespace="templates-core")),
    
    prefix_default_language=True
)


# API UI Docs URLs
urlpatterns += [
    path(f"{BASE_URL}/docs/", include("docs.urls", namespace="docs")),
]


# Django Browser Reload
urlpatterns += [
    path("__reload__/", include("django_browser_reload.urls")),
]


# Serving static and media files
urlpatterns += static(settings.STATIC_URL, serve, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)
