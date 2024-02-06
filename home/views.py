from django.shortcuts import render
from rest_framework.views import APIView
from home.serializer import RegistrationSerializer,AdminSerializer,DoctorSerializer,DoctorListSerializer,TokenSerializers,UsersSerializer,UpdateSerializer
from home.models import UserData,Doctor
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,IsAdminUser 
from rest_framework.decorators import permission_classes
 
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
                Doctor.objects.create(user=user)
                print("doctor created")
            return Response({'msg':'user created!'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
    
    
    
#     {
#     "username" : "das",
#     "email":"das@gmail.com",
#     "first_name" : "das",
#     "last_name":"n",
#     "password":"Das123456",
#     "confirm_password" : "Das123456",
#     "is_doctor":0
# }

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializers


# class LoginView(APIView):
    # def get(self,request,format=None):
    #     requested_user={
    #         "email":request.user.email,
    #         "username": request.user.username,
    #         "first_name": request.user.first_name,
    #         "last_name": request.user.last_name
    #     }
    #     return Response(requested_user)
    
    # def post(self,request,format=None):
    #     serializer = LoginSerializer(data=request.data)
    #     if serializer.is_valid():
    #         username = serializer.validated_data.get('username')
    #         password = serializer.validated_data.get('password')
    #         # user = authenticate(request, username=username, password=password)
    #         user = authenticate(request, username=username, password=password)
         
    #         if user is not None:
    #             print(user)
    #             refresh = RefreshToken.for_user(user)
    #             access_token = str(refresh.access_token)
    #             refresh_token = str(refresh)
    #             print("access_token",access_token)
    #             print("refresh_token",refresh_token)
    #             return Response({
    #                 'access_token':access_token,
    #                 'refresh_token':refresh_token,
    #             },status=status.HTTP_200_OK)
    #         return Response({"msg": "Doesn't exist. Or not found!"}, status=status.HTTP_204_NO_CONTENT) 
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DoctorView(APIView):
    def get(self,request):
        doctors = UserData.objects.filter(is_doctor=True)
        serializer = DoctorListSerializer(doctors, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
        

 
@permission_classes([IsAuthenticated])
class ProfileManagerView(APIView):
    
    def get(self, request ):
            user = UserData.objects.get(pk=request.user.id)
            serializer = UsersSerializer(user)   
            return Response({'msg':'user','data':serializer.data},status=status.HTTP_200_OK)
    
 
    def patch(self, request):
        try:
            print(request.data)
            user = request.user
            if user.is_doctor:
                doctor_profile = Doctor.objects.get(user=user)
                doctor_serializer = DoctorSerializer(doctor_profile, data=request.data, partial=True)

                if 'first_name' in request.data:
                    user.first_name = request.data['first_name']
                if 'last_name' in request.data:
                    user.last_name = request.data['last_name']
                if 'phone' in request.data:
                    user.phone = request.data['phone']
                user.save()  
                  
                if doctor_serializer.is_valid():
                    doctor_serializer.save()
                    return Response(doctor_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_profile = UserData.objects.get(id=request.user.id)
                serializer = UsersSerializer(user_profile, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserData.DoesNotExist:
            return Response({'detail': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Doctor.DoesNotExist:
            return Response({'detail': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self,request):
        try:
            user = UserData.objects.get(pk=request.user.id)
            user.delete()
            return Response({'msg':'deleted!'},status=status.HTTP_200_OK)
        except:
            return Response({'msg':'something wrong'},status=status.HTTP_400_BAD_REQUEST)
    

    
    
    
    
class AdminView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        user = UserData.objects.all()
        serializer = AdminSerializer(user,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        try:
            user = UserData.objects.get(id=pk)
            print(user)
            print(user.is_active,'b4')

            user.is_active = not user.is_active 
            print(user.is_active)

            user.save()
            serializer = AdminSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserData.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)   
    

