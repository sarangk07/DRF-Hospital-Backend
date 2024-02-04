from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,username,email,is_doctor=False,password=None,first_name=None,last_name=None):
        if not email:
            raise ValueError('User must have an email address')

        user=self.model(
            email=self.normalize_email(email),
            username = username,
            is_doctor=is_doctor,
            first_name=first_name,
            last_name = last_name,     
        )
        
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
    
    
class UsersDetails(AbstractBaseUser):
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField( max_length=50,null=True,blank=True)
    
    is_admin=models.BooleanField(default=False)    
    is_staff=models.BooleanField(default=False)    
    is_active=models.BooleanField(default=True)   
    is_superadmin=models.BooleanField(default=False)    
    is_doctor = models.BooleanField(default=False,null=True)
   


    
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS=['email']
    
    objects=UserManager()
    
    def __str__(self):
        return self.email
    
    

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
    
    
# class DoctorProfile(models.Model):
#     user = models.ForeignKey(UsersDetails, on_delete=models.CASCADE, related_name='doctorprofile')
#     hospital = models.CharField(max_length=50,blank=True,null=True)
#     department = models.CharField(max_length=50,null=True,blank=True)
#     speciality = models.CharField(max_length=50,blank=True,null=True)