from docs import views
from django.urls import re_path, path

app_name = "docs"

urlpatterns = [
   path("", views.api_documentation.with_ui("redoc", cache_timeout=0), name="api-schema-redoc"),
   path("ui/", views.api_documentation.with_ui("swagger", cache_timeout=0), name="api-schema-swagger-ui"),
   re_path(r"^swagger(?P<format>\.json|\.yaml)$", views.api_documentation.without_ui(cache_timeout=0), name="api-schema-json"),
]
