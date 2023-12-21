from core import views
from django.urls import path

app_name = "templates-core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]

urlpatterns += [
    path("set-language/<str:lang_code>/", views.set_language_view, name="set-language"),
]
