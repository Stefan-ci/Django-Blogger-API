from drf_yasg import openapi
from django.utils.translation import gettext_lazy as _

def posts_query_paramaters():
    page = openapi.Parameter("page", openapi.IN_QUERY, description=_("Page"), type=openapi.TYPE_INTEGER)
    return [page]


def categories_query_paramaters():
    page = openapi.Parameter("page", openapi.IN_QUERY, description=_("Page"), type=openapi.TYPE_INTEGER)
    return [page]

def comments_query_paramaters():
    page = openapi.Parameter("page", openapi.IN_QUERY, description=_("Page"), type=openapi.TYPE_INTEGER)
    return [page]
