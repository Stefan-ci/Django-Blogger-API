from drf_yasg import openapi
from rest_framework import status
from newsletter.models import Newsletter
from blogger_api.permissions import IsStaff
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.views import Response, APIView
from django.utils.translation import gettext_lazy as _
from newsletter.v1.serializers import NewsletterSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



class NewsletterListView(APIView):
    """ List newsletter """
    permission_classes = [IsAdminUser|IsStaff]
    
    @swagger_auto_schema(responses={200: NewsletterSerializer})
    def get(self, request, format=None):
        """ List all newsletters """
        newsletter = Newsletter.objects.all()
        paginator = Paginator(newsletter, 100)
        page = request.GET.get("page")
        newsletter_obj = paginator.get_page(page)
        try:
            newsletter = paginator.page(page)
        except PageNotAnInteger:
            newsletter = paginator.page(1)
        except EmptyPage:
            newsletter = paginator.page(paginator.num_pages)
        
        data = {
            "total_pages": paginator.num_pages,
            "current_page": newsletter_obj.number,
            "has_next": newsletter_obj.has_next(),
            "has_prev": newsletter_obj.has_previous(),
            "page_items_count": newsletter_obj.__len__(),
            "items_per_page": paginator.per_page,
            "data": NewsletterSerializer(newsletter_obj, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, description=_("Email"))
    }), responses={200: NewsletterSerializer})
    def post(self, request, format=None):
        """ Create a newsletter """
        serializer = NewsletterSerializer(data=request.data)
        email = serializer.initial_data["email"]
        if serializer.is_valid():
            serializer.save(is_deleted=False, is_subscribed=True)
            
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        elif Newsletter.objects.filter(email=email).exists():
            return Response({'detail': _("Vous étiez déjà inscrit à cette newsletter, Merci !")}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class NewsletterDetailView(APIView):
    """ Newsletter detail """
    permission_classes = [IsAdminUser|IsStaff]
    
    def get_object(self, pk: int):
        try:
            return Newsletter.objects.get(pk=pk)
        except Newsletter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    def get(self, request, pk, format=None):
        """ Detail a newsletter  """
        data = {
            "data": NewsletterSerializer(self.get_object(pk)).data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk, format=None):
        """ Update a newsletter instance """
        serializer = NewsletterSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        """ Delete/deactivate a newsletter """
        newsletter = self.get_object(pk)
        newsletter.is_deleted = True
        newsletter.is_subscribed = False
        newsletter.save()
        return Response({'detail': _("Newsletter supprimé avec succès !")}, status=status.HTTP_204_NO_CONTENT)
