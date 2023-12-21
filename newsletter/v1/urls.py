from django.urls import path
from newsletter.v1.views import NewsletterListView, NewsletterDetailView

app_name = "newsletter"

urlpatterns = [
    path("", NewsletterListView.as_view(), name="newsletter"), # List newsletter
    path("<int:pk>/", NewsletterDetailView.as_view(), name="newsletter-detail"), # Detail newsletter
]
