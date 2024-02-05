from rest_framework import serializers
from django.core.exceptions import ValidationError
from home.models import UserData


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

        