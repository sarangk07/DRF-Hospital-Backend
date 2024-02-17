from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import Token
from home.models import UserData,Doctor
from .models import Doctor
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
        username = data.get('username')
        
        if UserData.objects.filter(username=username).exists():
            raise ValidationError("User with this email already exists!")
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
        token = super().get_token(user)
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_admin'] = user.is_admin
        token['is_active'] = user.is_active
        token['is_blocked'] = user.is_blocked
        return token

    def validate(self, value):
        data = super().validate(value)
        user = self.user
        password = value.get('password')

        if user.is_blocked:
            raise ValidationError("User is blocked. Contact admin.")

        if not user.check_password(password):
            raise ValidationError("Incorrect password.")

        return data
        
     
     
        
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [ 'hospital', 'department', 'is_verified']        
           


class DoctorListSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(source='doctorprofile')

    class Meta:
        model = UserData
        fields = ['username', 'first_name', 'last_name', 'email', 'doctor']
                      


# old code 

class UsersSerializer(serializers.ModelSerializer):
    doctor_pro = DoctorProfileSerializer(allow_null=True , required=False,source='doctorprofile')
    class Meta:
        model = UserData
        fields = ('username','first_name','last_name','email','phone','is_active' ,'doctor_pro')
        

    def update(self, instance, validated_data):
        # Update user profile
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)

        # If user is doctor, update doctor profile.
        if instance.is_doctor:
            print("instanceeeeeeeeeeeeeeeeeeeeeeeeeeeeee",instance)
            doctor_profile_data = validated_data.get('doctorprofile')
            print("profileeeeeeeeeeeeeeeeeeee",doctor_profile_data)
            if doctor_profile_data:
                doctor_profile, created = Doctor.objects.get_or_create(user=instance)
                doctor_profile.hospital = doctor_profile_data.get('hospital', doctor_profile.hospital)
                doctor_profile.department = doctor_profile_data.get('department', doctor_profile.department)
                doctor_profile.save()

        instance.save()
        return instance
         
          
class AdminSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(source='doctorprofile')
    class Meta:
        model = UserData
        fields = ['pk','username', 'email', 'first_name', 'last_name', 'phone','is_doctor','is_active','is_admin','doctor']
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    
    
    


