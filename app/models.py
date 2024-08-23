from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import AbstractUser, BaseUserManager



class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        empId=kwargs.get('empId', None)
        # if not empId:
        #     raise ValueError('The empId field must not be empty.')
        if username is None:
            raise TypeError('User should have username')
        if email is None:
            raise TypeError('User should have email address')

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None,empId=None ,**extra_fields):

        if password is None:
            raise TypeError('Password should not be empty')

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        extra_fields['empId'] = empId
        # user.is_staff = True
        user.save()
        return user




class user(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=50)
    empId=models.CharField(max_length=10,  default='M1372', null= True)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=255, unique=True)
    
    pause=models.BooleanField(default=False)
    reset_token = models.CharField(null = True, max_length = 1000)
    objects = UserManager() 
    
    first_name = None
    last_name = None
    date_joined=None
    is_staff=None
    last_login=None
    
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        refresh_token['username'] = self.username

        refresh_token['email'] = self.email
        # refresh_token['empId'] = self.empId

        
        return {
            'refresh_token': str(refresh_token),
            'access_token': str(refresh_token.access_token)
        }