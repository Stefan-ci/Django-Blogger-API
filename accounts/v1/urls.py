from django.urls import path
from accounts.v1 import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "accounts"

urlpatterns = [
    path("list-users/", views.UserListView.as_view(), name="users-list"), # List users
    path("create-user/", views.CreateUserView.as_view(), name="users-register"), # Create user
    path("detail-user/me/", views.UserDetailView.as_view(), name="users-details"), # Detail user
    path("change-user/password/", views.ChangeUserPasswordView.as_view(), name="users-change-password"), # Change user password
    
    path("login/token/", views.LoginTokenObtainPairView.as_view(), name="login-token"),
    path("login/token/refresh/", TokenRefreshView.as_view(), name="login-token-refresh"),
]
