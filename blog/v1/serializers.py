from rest_framework import serializers
from blog.models import Post, Category, Comment
from accounts.v1.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)
    category = CategorySerializer(many=False)
    
    class Meta:
        model = Post
        fields = ["id", "title", "cover", "summary", "description", "date", "updated_on", "tags", "slug", "is_public",
            "uuid", "category", "extra_data", "author"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    post = PostSerializer(many=False)
    
    class Meta:
        model = Comment
        fields = ["id", "comment", "date", "updated_on", "is_public", "uuid", "extra_data", "user", "post"]



class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)
    category = CategorySerializer(many=False)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ["id", "title", "cover", "summary", "description", "date", "updated_on", "tags", "slug", "is_public",
            "uuid", "category", "extra_data", "author", "comments"]

    def get_comments(self, obj):
        return CommentSerializer(obj.comments(), many=True).data
