from django.shortcuts import render
from rest_framework.views import APIView
from home.serializer import RegistrationSerializer,AdminSerializer,DoctorProfileSerializer,TokenSerializers,UsersSerializer,DoctorListSerializer
from home.models import UserData,Doctor
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,IsAdminUser 
from rest_framework.decorators import permission_classes




# from rest_framework import generics

# class BlockUserView(generics.UpdateAPIView):
#     queryset = UserData.objects.all()
#     serializer_class = AdminSerializer

#     def perform_update(self, serializer):
#         serializer.instance.is_blocked = True
#         serializer.save()

# class UnblockUserView(generics.UpdateAPIView):
#     queryset = UserData.objects.all()
#     serializer_class = AdminSerializer

#     def perform_update(self, serializer):
#         serializer.instance.is_blocked = False
#         serializer.save()
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
            print(user)
            if user.is_doctor:
                Doctor.objects.create(user=user)
                print("doctor created")
            return Response({'msg':'user created!'},status=status.HTTP_201_CREATED)
        print("error")
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializers




 
@permission_classes([IsAuthenticated])
class ProfileManagerView(APIView):
    
    def get(self, request ):
            user = UserData.objects.get(pk=request.user.id)
            print(user)
            serializer = UsersSerializer(user)  
            print(serializer.data) 
            return Response({'msg':'user','data':serializer.data},status=status.HTTP_200_OK)    
      
        
    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        
        serializer = UsersSerializer(instance=user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request):
        try:
            user = UserData.objects.get(pk=request.user.id)
            user.delete()
            return Response({'msg':'deleted!'},status=status.HTTP_200_OK)
        except:
            return Response({'msg':'something wrong'},status=status.HTTP_400_BAD_REQUEST)
    


  
class AdminView(APIView):

    permission_classes = [IsAdminUser]
    
    # serilaizer = DoctorProfileSerializer
    # queryset = UserData.objects.filter(is_admin=False)
    
    
    def get(self,request):
        user = UserData.objects.all()
        serializer = AdminSerializer(user,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        try:
            user = UserData.objects.get(id=pk)
            print(user)
            # print(user.is_active,'b4')

            # user.is_active = not user.is_active
            user.is_blocked = not user.is_blocked 
            # print(user.is_active)
            print(user.is_blocked)

            user.save()
            serializer = AdminSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserData.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)   
        
        
 
 
class UserDoctorViews(APIView):
        def get(self,request):
            doctors = UserData.objects.filter(is_doctor=True)
            serializer = DoctorListSerializer(doctors,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        

            
        
        
    
    
        
        
        
        
        
        
        
        
        
        
        
        
    

