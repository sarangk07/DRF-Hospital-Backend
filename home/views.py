from django.shortcuts import render
from rest_framework.views import APIView
from home.serializer import RegistrationSerializer
from home.models import UserData
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
# Create your views here.

class Registration(APIView):
    def post(self,request,format = None):
        print(request.data)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            password = serializer.validated_data.get('password')
            is_doctor = serializer.validated_data.get('is_doctor')

            user = UserData.objects.create_user(
                email = email,
                username = username,
                password = password,
                is_doctor = is_doctor,
                first_name = first_name,
                last_name = last_name,
            
            )
            if user.is_doctor:
                print("doctor")
            return Response({'msg':'data added!'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
