from django.urls import path, include

app_name = "api-v1"

urlpatterns = [
    path("accounts/", include("accounts.v1.urls", namespace="accounts")),
    path("blog/", include("blog.v1.urls", namespace="blog")),
    path("contact/", include("contact.v1.urls", namespace="contact")),
    path("newsletter/", include("newsletter.v1.urls", namespace="newsletter")),
]
