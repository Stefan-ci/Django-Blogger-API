from accounts.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class ChangeUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": _("Les mots ne concordent pas.")})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"], email=validated_data["email"], is_active=True)
        user.set_password(validated_data["password"])
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff", "is_active", "is_superuser",
            "account_confirmed", "phone_number", "gender", "country", "region", "city", "address", "address_2", "zip_code",
            "age", "website", "bio", "avatar", "uuid", "date_joined", "last_login", "updated_on", "extra_data"]
    
    def get_country(self, obj) -> str:
        return obj.country.name



class UpdateUserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "gender", "country", "region", "city", "address",
            "address_2", "zip_code", "age", "website", "bio", "avatar", "extra_data"]
