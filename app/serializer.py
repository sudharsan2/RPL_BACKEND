from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import user
from rest_framework.exceptions import AuthenticationFailed



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    
    # roles = serializers.PrimaryKeyRelatedField(queryset=UserRoles.objects.all(), required=True)

    class Meta:
        model = user
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
    
        if not username.isalnum():
            raise serializers.ValidationError('Username should not contain alpha numeric characters')

        return attrs

    def create(self, validated_data):
        return user.objects.create_user(**validated_data)
    
# class userRolesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=UserRoles
#         fields='__all__'


class loginSerializer(serializers.ModelSerializer):
    
    password=serializers.CharField(max_length=255, write_only=True)
    username=serializers.CharField(max_length=255)
    
            
    class Meta:
        model=user
        fields=['username','password', 'tokens']
        
    def validate(self, obj):
        name=obj.get('username', '')
        passWord=obj.get('password', '')
        
        
        user = authenticate(username=name, password=passWord, is_active=True)
        
        if not user:
            raise AuthenticationFailed('Invalid Credentials')
            
        if not user.is_active:
            raise AuthenticationFailed('Account not valid, Contact admin')

       
        
        return {
            'email': user.email,
            'username': user.username,
            'id': user.id,
            'tokens': user.tokens()
        }

    