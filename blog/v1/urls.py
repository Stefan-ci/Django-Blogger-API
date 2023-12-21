from django.urls import path
from blog.v1.views import (
    PostListView, CategoryListView, CategoryDetailView, CommentDetailView, PostDetailView, CommentListView
)

app_name = "blog"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts-list"), # Posts list
    path("posts/<int:pk>/", PostDetailView.as_view(), name="posts-detail"), # Posts detail
    
    path("categories/", CategoryListView.as_view(), name="categories-list"), # Categories list
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="categories-detail"), # Categories detail
    
    path("comments/", CommentListView.as_view(), name="comments-list"), # Comments list
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comments-detail"), # Comments detail
]
