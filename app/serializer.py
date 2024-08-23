from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import user
from rest_framework.exceptions import AuthenticationFailed
from .models import (
    WorkOrderHeader, ProductionDetail, MaterialDetail, RawMaterial,
    ScrapDetail, MachineParameter, LineClearance, PolyWastageDetail
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





class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class MaterialDetailSerializer(serializers.ModelSerializer):
    raw_material = RawMaterialSerializer()

    class Meta:
        model = MaterialDetail
        fields = '__all__'

class ProductionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionDetail
        fields = '__all__'

class ScrapDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapDetail
        fields = '__all__'

class MachineParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineParameter
        fields = '__all__'

class LineClearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineClearance
        fields = '__all__'

class PolyWastageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolyWastageDetail
        fields = '__all__'

class WorkOrderHeaderSerializer(serializers.ModelSerializer):
    production_details = ProductionDetailSerializer(many=True)
    material_details = MaterialDetailSerializer(many=True)
    scrap_details = ScrapDetailSerializer()
    machine_parameters = MachineParameterSerializer()
    line_clearance = LineClearanceSerializer()
    poly_wastage_details = PolyWastageDetailSerializer()

    class Meta:
        model = WorkOrderHeader
        fields = '__all__'

    def create(self, validated_data):
       
        production_details_data = validated_data.pop('production_details')
        material_details_data = validated_data.pop('material_details')
        scrap_details_data = validated_data.pop('scrap_details')
        machine_parameters_data = validated_data.pop('machine_parameters')
        line_clearance_data = validated_data.pop('line_clearance')
        poly_wastage_details_data = validated_data.pop('poly_wastage_details')

        
        work_order_header = WorkOrderHeader.objects.create(**validated_data)

        
        for production_data in production_details_data:
            ProductionDetail.objects.create(work_order_header=work_order_header, **production_data)

        
        for material_data in material_details_data:
            raw_material_data = material_data.pop('raw_material')
            raw_material = RawMaterial.objects.create(**raw_material_data)
            MaterialDetail.objects.create(work_order_header=work_order_header, raw_material=raw_material, **material_data)

        
        ScrapDetail.objects.create(work_order_header=work_order_header, **scrap_details_data)
        MachineParameter.objects.create(work_order_header=work_order_header, **machine_parameters_data)
        LineClearance.objects.create(work_order_header=work_order_header, **line_clearance_data)
        PolyWastageDetail.objects.create(work_order_header=work_order_header, **poly_wastage_details_data)

        return work_order_header
