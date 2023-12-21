from drf_yasg import openapi
from accounts.models import User
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import Response, APIView
from django.utils.translation import gettext_lazy as _
from accounts.v1.utils import accounts_query_paramaters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from blogger_api.permissions import IsNotAuthenticated, IsStaff
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from accounts.v1.serializers import (
    UserSerializer,
    UpdateUserSerilaizer,
    CreateUserSerializer,
    ChangeUserPasswordSerializer,
    LoginTokenObtainPairSerializer
)


class LoginTokenObtainPairView(TokenObtainPairView):
    """ Token based authentication """
    serializer_class = LoginTokenObtainPairSerializer


class UserListView(APIView):
    """ List all users from database (active and inactive) """
    permission_classes = [IsAdminUser|IsStaff]
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        return User.objects.all()
    
    @swagger_auto_schema(responses={200: UserSerializer}, manual_parameters=accounts_query_paramaters())
    def get(self, request, format=None):
        """ Get users list **Admin/Staff account required** """
        paginator = Paginator(self.get_queryset(), 100)
        page = request.GET.get("page")
        users_obj = paginator.get_page(page)
        try:
            paginator.page(page)
        except PageNotAnInteger:
            paginator.page(1)
        except EmptyPage:
            paginator.page(paginator.num_pages)
        
        data = {
            "total_pages": paginator.num_pages,
            "current_page": users_obj.number,
            "has_next": users_obj.has_next(),
            "has_prev": users_obj.has_previous(),
            "page_items_count": users_obj.__len__(),
            "items_per_page": paginator.per_page,
            "data": UserSerializer(users_obj, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)





class UserDetailView(APIView):
    """ Get details of the current logged in user """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self) -> User:
        return self.request.user
    
    @swagger_auto_schema(responses={200: UserSerializer})
    def get(self, request, format=None):
        """ Get details of the current (logged in) user """
        data = {
            "data": UserSerializer(self.get_object(), many=False).data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, description=_("Prénom")),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description=_("Nom")),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description=_("Email")),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description=_("N° de téléphone (au format +44…)")),
        "gender": openapi.Schema(type=openapi.TYPE_STRING, description=_("Soit 'male', 'female' ou 'undefined'")),
        "country": openapi.Schema(type=openapi.TYPE_STRING, description=_("Pays (code ISO du pays (Ex: US, DE, FR, CI))")),
        "region": openapi.Schema(type=openapi.TYPE_STRING, description=_("Région")),
        "city": openapi.Schema(type=openapi.TYPE_STRING, description=_("Ville")),
        "address": openapi.Schema(type=openapi.TYPE_STRING, description=_("Adresse")),
        "address_2": openapi.Schema(type=openapi.TYPE_STRING, description=_("2e adresse")),
        "zip_code": openapi.Schema(type=openapi.TYPE_INTEGER, description=_("Code postal (5 chiffres maxi)")),
        "age": openapi.Schema(type=openapi.TYPE_INTEGER, description=_("Âge")),
        "website": openapi.Schema(type=openapi.TYPE_STRING, description=_("Site web")),
        "bio": openapi.Schema(type=openapi.TYPE_STRING, description=_("Biographie")),
        "avatar": openapi.Schema(type=openapi.TYPE_FILE, description=_("Avatar")),
        "extra_data": openapi.Schema(type=openapi.TYPE_OBJECT, description=_("Données extra (Format JSON)")),
    }), responses={200: UserSerializer})
    def put(self, request, format=None):
        """ Update (logged in) user's infos """
        user: User = request.user
        serializer = UpdateUserSerilaizer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "data": UserSerializer(user, many=False).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, format=None):
        """ Delete/deactivate the current (logged in) user """
        user: User = request.user
        
        user.is_active = False
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return Response({'detail': _("Utilisateur supprimé avec succès")}, status=status.HTTP_204_NO_CONTENT)






class CreateUserView(APIView):
    """ User creation """
    permission_classes = [IsNotAuthenticated]
    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "username": openapi.Schema(type=openapi.TYPE_STRING, description=_("Pseudo")),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description=_("Email")),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description=_("Mot de passe")),
        "password2": openapi.Schema(type=openapi.TYPE_STRING, description=_("Confirmer le mot de passe")),
    }), responses={200: UserSerializer})
    def post(self, request, format=None):
        """ Create a new user (register) """
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = {
                "data": UserSerializer(user, many=False).data,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ChangeUserPasswordView(APIView):
    """ Change logged in user's password """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "old_password": openapi.Schema(type=openapi.TYPE_STRING, description=_("Old password")),
        "new_password": openapi.Schema(type=openapi.TYPE_STRING, description=_("New password")),
    }))
    def put(self, request, format=None):
        """ Update current password """
        self.object: User = request.user
        serializer = ChangeUserPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": [_("Mot de passe incorrect")]}, status=status.HTTP_400_BAD_REQUEST)
                
            # Set new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {
                    "detail": _("Mot de passe modifié avec succès"),
                    "data": UserSerializer(self.object, many=False).data,
                },
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
