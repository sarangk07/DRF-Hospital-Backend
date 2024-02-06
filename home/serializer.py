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
    
    # def create(self, validated_data):
    #     user = UserData.objects.create_user(
    #             email = validated_data['email'],
    #             username = validated_data['username'],
    #             password = validated_data['password'],
    #             is_doctor = validated_data['is_doctor'],
    #             first_name = validated_data['first_name'],
    #             last_name = validated_data['last_name'],
    #         )
    #     # if user.is_doctor:
    #     #     print("doctor--------------------")
    #     return user


class TokenSerializers(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(user)
        token = super(TokenSerializers,cls).get_token(user)
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_admin'] = user.is_admin
        return token

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         token['is_doctor'] = user.is_doctor
#         token['is_admin'] = user.is_admin
#         token['is_active'] =user.is_active
#         return token



# class LoginSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(style={'input_type':{'password'}})
#     class Meta:
#         model = UserData
#         fields = ['username','password']
        


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [ 'hospital', 'department', 'is_verified']


class UserProfileSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(allow_null=True, required=False)
    class Meta:
        model = UserData
        fields = ['username', 'first_name', 'last_name', 'email', 'phone','doctor']



class DoctorListSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(source='doctorprofile',many=True) 
    class Meta:
        model = UserData
        fields = ['username', 'first_name', 'last_name','doctor']











class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['hospital','department', 'is_verified']
        
        
        
        

        
        
        
        
class UsersSerializer(serializers.ModelSerializer):
    doctors_pro = DoctorSerializer(allow_null=True , required=False)
    print(doctors_pro)
    class Meta:
        model = UserData
        fields = ('username','first_name','last_name','email','phone','is_active' ,'doctors_pro')
          
          
          
class UpdateSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer()
    # print(doctors)
    class Meta:
      model = UserData
      fields = ('id','first_name', 'last_name','username', 'email','doctors')        











class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['pk','username', 'email', 'first_name', 'last_name', 'phone','is_doctor','is_active','is_admin']











# class DoctorSerilaizer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = '__all__'
        