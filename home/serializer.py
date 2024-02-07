from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import Token
from home.models import UserData,Doctor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model  = UserData
        fields = ['username','email','first_name','last_name','password','confirm_password','is_doctor']
        
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        email = data.get('email')
        
        if UserData.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists!")
        if password != confirm_password:
            raise ValidationError("password and confirm_password doesn't match!")        
        return data


#login
class TokenSerializers(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(user)
        token = super(TokenSerializers,cls).get_token(user)
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_admin'] = user.is_admin
        return token

        
        
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [ 'hospital', 'department', 'is_verified']        
           


# class DoctorSerializer(serializers.ModelSerializer):
#     doctor = DoctorProfileSerializer(source='doctorprofile', many=True)
#     class Meta:
#         model = Doctor
#         fields = ['hospital','department', 'is_verified']
                  


       
class UsersSerializer(serializers.ModelSerializer):
    doctor_pro = DoctorProfileSerializer(allow_null=True , required=False,source='doctorprofile')
    class Meta:
        model = UserData
        fields = ('username','first_name','last_name','email','phone','is_active' ,'doctor_pro')
          
          
          
class UpdateSerializer(serializers.ModelSerializer):
    doctors = DoctorProfileSerializer()
    class Meta:
      model = UserData
      fields = ('id','first_name', 'last_name','username', 'email','doctors')        


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['pk','username', 'email', 'first_name', 'last_name', 'phone','is_doctor','is_active','is_admin']

