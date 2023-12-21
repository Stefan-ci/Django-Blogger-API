from drf_yasg import openapi
from django.conf import settings
from django.utils.html import format_html
from drf_yasg.views import get_schema_view
from blogger_api.permissions import IsStaff
from rest_framework.permissions import IsAdminUser
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication, TokenAuthentication



api_description = format_html(_(f"""
        Documentation officielle de l'API de <strong>{settings.SITE_NAME}</strong>.
    """))

_license = _("""
        Aucune licence. Il est formellement interdit de consulter, vendre, copier ou reproduire ce projet 
        si l'on n'a pas reçu une autorisation express.
    """)

api_documentation = get_schema_view(
    openapi.Info(
        title=f"{settings.SITE_NAME}",
        default_version=f"{settings.API_CURRENT_VERSION}",
        description=api_description,
        terms_of_service="",
        contact=openapi.Contact(name="Stefan-ci", url="https://github.com/Stefan-ci", email="kiuv.abraj@gmail.com"),
        license=openapi.License(name=_license),
    ),
    public=False,
    permission_classes=[IsAdminUser|IsStaff], # You may want to restrict access by adding only necessary perm classes
    authentication_classes=[BasicAuthentication, TokenAuthentication, JWTAuthentication]
)
