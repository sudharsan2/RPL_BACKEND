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
    



class WorkOrderHeader(models.Model):
    work_order_no = models.CharField(max_length=255)
    customer = models.CharField(max_length=255)
    job_name = models.CharField(max_length=255)
    sleeve_size = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    produced = models.CharField(max_length=255)
    balance = models.CharField(max_length=255)
    operator_name = models.CharField(max_length=255)
    assistant_name = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    mc_name = models.CharField(max_length=255)
    shift = models.CharField(max_length=255)
    mc_speed = models.CharField(max_length=255)
    production_weight = models.CharField(max_length=255)
    dyan_level = models.CharField(max_length=255)


class ProductionDetail(models.Model):
    work_order_header = models.ForeignKey(WorkOrderHeader, related_name='production_details', on_delete=models.CASCADE)
    printed_roll_no = models.CharField(max_length=255)
    printing_op_name = models.CharField(max_length=255)
    printed_input_roll_kgs = models.CharField(max_length=255)
    sup_name = models.CharField(max_length=255)
    sup_roll_no = models.CharField(max_length=255)
    net_wt = models.CharField(max_length=255)
    output_roll_no = models.CharField(max_length=255)
    output_roll_wt_kgs = models.CharField(max_length=255)
    output_roll_mtrs = models.CharField(max_length=255)
    starting_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    adh_gsm = models.CharField(max_length=255)


class RawMaterial(models.Model):
    details = models.CharField(max_length=255)
    nco_supplier = models.CharField(max_length=255)
    nco_grade = models.CharField(max_length=255)
    nco_bath_no = models.CharField(max_length=255)
    oh_supplier = models.CharField(max_length=255)
    oh_grade = models.CharField(max_length=255)
    oh_bath_no = models.CharField(max_length=255)


class MaterialDetail(models.Model):
    work_order_header = models.ForeignKey(WorkOrderHeader, related_name='material_details', on_delete=models.CASCADE)
    sl_no = models.CharField(max_length=255)
    raw_material = models.OneToOneField(RawMaterial, on_delete=models.CASCADE)
    size = models.CharField(max_length=255)
    mc = models.CharField(max_length=255)
    input = models.CharField(max_length=255)
    return_material = models.CharField(max_length=255)
    used = models.CharField(max_length=255)
    line_clearance = models.CharField(max_length=255)
    supplier = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    bath_no = models.CharField(max_length=255)
    ratio = models.CharField(max_length=255, blank=True)
    input_qty = models.CharField(max_length=255, blank=True)


class ScrapDetail(models.Model):
    work_order_header = models.OneToOneField(WorkOrderHeader, related_name='scrap_details', on_delete=models.CASCADE)
    plain_pe_wastage = models.CharField(max_length=255)
    printed_wastage = models.CharField(max_length=255)
    packing_waste = models.CharField(max_length=255)
    lamination_waste = models.CharField(max_length=255)
    total = models.CharField(max_length=255)


class MachineParameter(models.Model):
    work_order_header = models.OneToOneField(WorkOrderHeader, related_name='machine_parameters', on_delete=models.CASCADE)
    unwinder1 = models.CharField(max_length=255)
    unwinder2 = models.CharField(max_length=255)
    rewinder = models.CharField(max_length=255)
    coating_temp = models.CharField(max_length=255)
    nip_temp = models.CharField(max_length=255)
    nco_temp = models.CharField(max_length=255)
    oh_temp = models.CharField(max_length=255)
    coater_current = models.CharField(max_length=255, blank=True)
    nip_pressure = models.CharField(max_length=255)


class LineClearance(models.Model):
    work_order_header = models.OneToOneField(WorkOrderHeader, related_name='line_clearance', on_delete=models.CASCADE)
    solvent = models.BooleanField(default=False)
    cylinder = models.BooleanField(default=False)
    rubber_roller = models.BooleanField(default=False)
    dr_blade = models.BooleanField(default=False)
    raw_material = models.BooleanField(default=False)
    mc_surroundings = models.BooleanField(default=False)
    waste_matl = models.BooleanField(default=False)
    printed_matl = models.BooleanField(default=False)


class PolyWastageDetail(models.Model):
    work_order_header = models.OneToOneField(WorkOrderHeader, related_name='poly_wastage_details', on_delete=models.CASCADE)
    damage = models.CharField(max_length=255)
    wrinkle = models.CharField(max_length=255)
    core_end = models.CharField(max_length=255)
