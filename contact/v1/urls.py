from django.urls import path
from contact.v1.views import ContacttListView, ContacttDetailtView

app_name = "contact"

urlpatterns = [
    path("", ContacttListView.as_view(), name="contact-list"),
    path("<int:pk>/", ContacttDetailtView.as_view(), name="contact-detail"),
]
