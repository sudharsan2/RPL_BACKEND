from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework  import generics, status, views, permissions, parsers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import (RegisterSerializer, loginSerializer,WorkOrderHeaderSerializer)
from django.shortcuts import get_object_or_404
from .models import WorkOrderHeader
from rest_framework_simplejwt.tokens import RefreshToken
from .models import user

# Create your views here.

class RegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        userpayload = request.data

        serializer = self.serializer_class(data=userpayload)
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        
        user_data = serializer.data
        user_obj = user.objects.get(email=user_data.get('email'))
        token = RefreshToken.for_user(user_obj).access_token
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class=loginSerializer
    def post(self, request):
         user = request.data
         serializer = self.serializer_class(data=user)
         serializer.is_valid(raise_exception=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
    
# class submitForm(APIView):
#     def post(self, request):
#         body = request.data
#         return Response(body, status= status.HTTP_200_OK)
    


class WorkOrderAPIView(APIView):
    def post(self, request):
        serializer = WorkOrderHeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        work_order = get_object_or_404(WorkOrderHeader, id=id)
        serializer = WorkOrderHeaderSerializer(work_order)
        return Response(serializer.data, status=status.HTTP_200_OK)

