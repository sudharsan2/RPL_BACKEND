from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import user
from rest_framework.exceptions import AuthenticationFailed
from .models import (
    WorkOrderHeader, ProductionDetail, MaterialDetail, RawMaterial,
    ScrapDetail, MachineParameter, LineClearance, PolyWastageDetail,NcoAndOh
)



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)

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



# serializers.py

from rest_framework import serializers
from .models import ProductionDetail

class ProductionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionDetail
        fields = "__all__"

class NcoAndOhSerializer(serializers.ModelSerializer):
    class Meta:
        model = NcoAndOh
        fields = "__all__"

class ScrapDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapDetail
        fields = "__all__"

class machineParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineParameter
        fields = "__all__"

class LineClearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineClearance
        fields = "__all__"

class PolyWastageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolyWastageDetail
        fields = "__all__"

class WorkOrderHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderHeader
        fields = [
            'id',
            'workOrderNo',
            'customer',
            'jobName',
            'sleeveSize',
            'target',
            'produced',
            'balance',
            'operatorName',
            'assistantName',
            'date',
            'mcName',
            'shift',
            'mcSpeed',
            'productionWeight',
        ]