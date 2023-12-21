from drf_yasg import openapi
from rest_framework import status
from blogger_api.permissions import IsStaff
from drf_yasg.utils import swagger_auto_schema
from blog.models import Post, Category, Comment
from rest_framework.permissions import IsAdminUser
from rest_framework.views import Response, APIView
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.v1.utils import posts_query_paramaters, categories_query_paramaters, comments_query_paramaters
from blog.v1.serializers import PostSerializer, CategorySerializer, CommentSerializer, PostDetailSerializer



class PostListView(APIView):
    """ List all blog posts """
    permission_classes = [IsAdminUser|IsStaff]
    
    def get_queryset(self):
        return Post.objects.all()
    
    @swagger_auto_schema(responses={200: PostSerializer}, manual_parameters=posts_query_paramaters())
    def get(self, request, format=None):
        """ Get posts list """
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
            "data": PostSerializer(users_obj, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, description=_("Titre")),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, description=_("Catégorie (ID de la catégorie)")),
        "cover": openapi.Schema(type=openapi.TYPE_FILE, description=_("Couverture (image)")),
        "summary": openapi.Schema(type=openapi.TYPE_STRING, description=_("Résumé du poste")),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description=_("Contenu du poste")),
        "tags": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description=_("Mots clés (séparés par des virgules)"),
            items=openapi.Items(type=openapi.TYPE_STRING)
        ),
    }), responses={200: CategorySerializer})
    def post(self, request, format=None):
        """ Create new post """
        if not self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                category = Category.objects.get(pk=serializer.validated_data["category"])
            except Post.DoesNotExist:
                return Response(
                    {"detail": _(f"La catégorie avec l'identifiant {serializer.validated_data['category']} n'existe pas")},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer.save(category=category, author=self.request.user)
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class PostDetailView(APIView):
    """ Post Detail """
    permission_classes = [IsAdminUser|IsStaff]
    
    def get_object(self, pk: int):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(responses={200: PostDetailSerializer})
    def get(self, request, pk, format=None):
        """ Get post detail """
        data = {
            "data": PostDetailSerializer(self.get_object(pk=pk), many=False).data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, description=_("Titre")),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, description=_("Catégorie (ID de la catégorie)")),
        "cover": openapi.Schema(type=openapi.TYPE_FILE, description=_("Couverture (image)")),
        "summary": openapi.Schema(type=openapi.TYPE_STRING, description=_("Résumé du poste")),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description=_("Contenu du poste")),
        "tags": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description=_("Mots clés (séparés par des virgules)"),
            items=openapi.Items(type=openapi.TYPE_STRING)
        ),
    }), responses={200: PostDetailSerializer})
    def put(self, request, pk, format=None):
        """ Update post """
        serializer = PostDetailSerializer(self.get_object(pk=pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        """ Delete/deactivate post """
        post = self.get_object(pk=pk)
        post.is_public = False
        post.save()
        return Response({'detail': _("Poste supprimé avec succès")}, status=status.HTTP_204_NO_CONTENT)










class CategoryListView(APIView):
    """ List all blog categories """
    permission_classes = [IsAdminUser|IsStaff]
    
    def get_queryset(self):
        return Category.objects.all()
    
    @swagger_auto_schema(responses={200: CategorySerializer}, manual_parameters=categories_query_paramaters())
    def get(self, request, format=None):
        """ Get categories list """
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
            "data": CategorySerializer(users_obj, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description=_("Catégorie")),
    }), responses={200: CategorySerializer})
    def post(self, request, format=None):
        """ Create category """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class CategoryDetailView(APIView):
    """ Category Detail """
    permission_classes = [IsAdminUser|IsStaff]
    
    def get_object(self, pk: int):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(responses={200: CategorySerializer})
    def get(self, request, pk, format=None):
        """ Get category detail """
        data = {
            "data": CategorySerializer(self.get_object(pk=pk), many=False).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description=_("Catégorie")),
    }), responses={200: CategorySerializer})
    def put(self, request, pk, format=None):
        """ Update category """
        serializer = CategorySerializer(self.get_object(pk=pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        """ Delete/deactivate category """
        category = self.get_object(pk=pk)
        category.is_active = False
        category.save()
        return Response({'detail': _("Catégorie supprimée avec succès")}, status=status.HTTP_204_NO_CONTENT)










class CommentListView(APIView):
    """ List all blog comments from database """
    permission_classes = [IsAdminUser|IsStaff]
    
    def get_queryset(self):
        return Comment.objects.all()
    
    @swagger_auto_schema(responses={200: CommentSerializer}, manual_parameters=comments_query_paramaters())
    def get(self, request, format=None):
        """ Get comments list """
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
            "data": CommentSerializer(users_obj, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "comment": openapi.Schema(type=openapi.TYPE_STRING, description=_("Commentaire")),
        "post": openapi.Schema(type=openapi.TYPE_INTEGER, description=_("Poste (ID du poste)")),
    }), responses={200: CommentSerializer})
    def post(self, request, format=None):
        """ Create comment """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                post = Post.objects.get(pk=serializer.validated_data["post"])
            except Post.DoesNotExist:
                return Response(
                    {"detail": _(f"Le poste avec l'identifiant {serializer.validated_data['post']} n'existe pas")},
                    status=status.HTTP_404_NOT_FOUND
                )
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            serializer.save(post=post, user=user)
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CommentDetailView(APIView):
    """ Comment Detail """
    permission_classes = [IsAdminUser|IsStaff]
    
    def get_object(self, pk: int):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(responses={200: CommentSerializer})
    def get(self, request, pk, format=None):
        """ Get comment detail """
        data = {
            "data": CommentSerializer(self.get_object(pk=pk), many=False).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "comment": openapi.Schema(type=openapi.TYPE_STRING, description=_("Commentaire")),
    }), responses={200: CommentSerializer})
    def put(self, request, pk, format=None):
        """ Update Comment """
        serializer = CommentSerializer(self.get_object(pk=pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        """ Delete/deactivate Comment """
        comment = self.get_object(pk=pk)
        comment.is_public = False
        comment.save()
        return Response({'detail': _("Commentaire supprimé avec succès")}, status=status.HTTP_204_NO_CONTENT)
