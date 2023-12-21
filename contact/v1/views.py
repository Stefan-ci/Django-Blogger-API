from drf_yasg import openapi
from rest_framework import status
from contact.models import Contact
from blogger_api.permissions import IsStaff
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.views import Response, APIView
from contact.v1.serializers import ContactSerializer
from django.utils.translation import gettext_lazy as _
from contact.v1.utils import  contacts_query_paramaters
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class ContacttListView(APIView):
    """ List all contacts """
    permission_classes = [IsAdminUser|IsStaff]
    
    def get_queryset(self):
        return Contact.objects.all()
    
    @swagger_auto_schema(responses={200: ContactSerializer}, manual_parameters=contacts_query_paramaters())
    def get(self, request, format=None):
        """ Get contacts list """
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
            "data": ContactSerializer(users_obj, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "subject": openapi.Schema(type=openapi.TYPE_STRING, description=_("Objet")),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description=_("Email")),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description=_("Nom & Prénom")),
        "message": openapi.Schema(type=openapi.TYPE_STRING, description=_("Message")),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description=_("N° de téléphone")),
        "extra_data": openapi.Schema(type=openapi.TYPE_OBJECT, description=_("Autres infos (Format JSON)")),
    }), responses={200: ContactSerializer})
    def post(self, request, format=None):
        """ Create contact """
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class ContacttDetailtView(APIView):
    """ Contact Detail """
    permission_classes = [IsAdminUser|IsStaff]
    
    def get_object(self, pk: int):
        try:
            return Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(responses={200: ContactSerializer})
    def get(self, request, pk, format=None):
        """ Get contact detail """
        data = {
            "data": ContactSerializer(self.get_object(pk=pk), many=False).data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "subject": openapi.Schema(type=openapi.TYPE_STRING, description=_("Objet")),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description=_("Email")),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description=_("Nom & Prénom")),
        "message": openapi.Schema(type=openapi.TYPE_STRING, description=_("Message")),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description=_("N° de téléphone")),
        "is_answered": openapi.Schema(type=openapi.TYPE_BOOLEAN, description=_("Déjà répondu")),
        "extra_data": openapi.Schema(type=openapi.TYPE_OBJECT, description=_("Autres infos (Format JSON)")),
    }), responses={200: ContactSerializer})
    def put(self, request, pk, format=None):
        """ Update contact """
        serializer = ContactSerializer(self.get_object(pk=pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        """ Delete contact """
        contact = self.get_object(pk=pk)
        contact.delete()
        return Response({'detail': _("Contact supprimé avec succès")}, status=status.HTTP_204_NO_CONTENT)
