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
    






class ProductionDetail(models.Model):
    printedRollNo = models.CharField(max_length=255, db_column='printedRollNo', null=True)
    printingOpName = models.CharField(max_length=255, db_column='printingOpName', null=True)
    printedInputRollKgs = models.CharField(max_length=255, db_column='printedInputRollKgs', null=True)
    supName = models.CharField(max_length=255, db_column='supName', null=True)
    supRollNo = models.CharField(max_length=255, db_column='supRollNo', null=True)
    netWt = models.CharField(max_length=255, db_column='netWt', null=True)
    outputRollNo = models.CharField(max_length=255, db_column='outputRollNo', null=True)
    outputRollWtKgs = models.CharField(max_length=255, db_column='outputRollWtKgs', null=True)
    outputRollMtrs = models.CharField(max_length=255, db_column='outputRollMtrs', null=True)
    startingTime = models.CharField(max_length=255, db_column='startingTime', null=True)
    endTime = models.CharField(max_length=255, db_column='endTime', null=True)
    adhGsm = models.CharField(max_length=255, db_column='adhGsm', null=True)
 
 
class NcoAndOh(models.Model):
   supplier = models.CharField(max_length=255, db_column='supplier', null=True)
   grade = models.CharField(max_length=255, db_column='grade', null=True)
   bathNo = models.CharField(max_length=255, db_column='bathNo', null=True)
 
 
class RawMaterial(models.Model):
    details = models.CharField(max_length=255, null=True)
    nco = models.OneToOneField(NcoAndOh, on_delete=models.CASCADE, related_name='raw_material_nco', null=True)
    oh = models.OneToOneField(NcoAndOh, on_delete=models.CASCADE, related_name='raw_material_oh', null=True)
 
 
class MaterialDetail(models.Model):
    slNo = models.CharField(max_length=255, db_column='slNo', null=True)
    rawMaterial = models.OneToOneField(RawMaterial, on_delete=models.CASCADE, null=True)
    size = models.CharField(max_length=255, null=True)
    mc = models.CharField(max_length=255, null=True)
    input = models.CharField(max_length=255, null=True)
    returnMaterial = models.CharField(max_length=255, db_column='return', null=True)  # Changed from 'return' to 'returnMaterial'
    used = models.CharField(max_length=255, null=True)
    lineClearance = models.CharField(max_length=255, db_column='lineClearance', null=True)
    supplier = models.CharField(max_length=255, null=True)
    grade = models.CharField(max_length=255, null=True)
    bathNo = models.CharField(max_length=255, null=True)
    ratio = models.CharField(max_length=255, blank=True, null=True)
    inputQty = models.CharField(max_length=255, blank=True, db_column='inputQty', null=True)
 
 
class ScrapDetail(models.Model):
    plainPEWastage = models.CharField(max_length=255, db_column='plainPEWastage', null=True)
    printedWastage = models.CharField(max_length=255, db_column='printedWastage', null=True)
    packingWaste = models.CharField(max_length=255, db_column='packingWaste', null=True)
    laminationWaste = models.CharField(max_length=255, db_column='laminationWaste', null=True)
    total = models.CharField(max_length=255, null=True)


class breakDownDetail(models.Model):
    sleeveChange = models.CharField(max_length=255, db_column='sleeveChange', null=True)
    cleaning = models.CharField(max_length=255, db_column='cleaning', null=True)
    totalProdnMin = models.CharField(max_length=255, db_column='totalProdnMin', null=True)
    jobSettingMin = models.CharField(max_length=255, db_column='jobSettingMin', null=True)
    rollChangeMin = models.CharField(max_length=255, db_column='rollChangeMin', null=True)
    noPlanning = models.CharField(max_length=255, db_column='noPlanning', null=True)
    breakDownMin = models.CharField(max_length=255, db_column='breakDownMin', null=True)
    powerCut = models.CharField(max_length=255, db_column='powerCut', null=True)
    tagRemove = models.CharField(max_length=255, db_column='tagRemove', null=True)
    total = models.CharField(max_length=255, null=True)

 
class MachineParameter(models.Model):
    unwinder1 = models.CharField(max_length=255, null=True)
    unwinder2 = models.CharField(max_length=255, null=True)
    rewinder = models.CharField(max_length=255, null=True)
    coatingTemp = models.CharField(max_length=255, db_column='coatingTemp', null=True)
    nipTemp = models.CharField(max_length=255, db_column='nipTemp', null=True)
    lc1 = models.CharField(max_length=255, null=True)
    ncoTemp = models.CharField(max_length=255, db_column='ncoTemp', null=True)
    ohTemp = models.CharField(max_length=255, db_column='ohTemp', null=True)
    coaterCurrent = models.CharField(max_length=255, blank=True, db_column='coaterCurrent', null=True)
    nipPressure = models.CharField(max_length=255, db_column='nipPressure', null=True)
 
 
class LineClearance(models.Model):
    solvent = models.BooleanField(default=False, null=True)
    cylinder = models.BooleanField(default=False, null=True)
    rubberRoller = models.BooleanField(default=False, db_column='rubberRoller', null=True)
    drBlade = models.BooleanField(default=False, db_column='drBlade', null=True)
    rawMaterial = models.BooleanField(default=False, db_column='rawMaterial', null=True)
    mcSurroundings = models.BooleanField(default=False, db_column='mcSurroundings', null=True)
    wasteMatl = models.BooleanField(default=False, db_column='wasteMatl', null=True)
    printedMatl = models.BooleanField(default=False, db_column='printedMatl', null=True)
 
 
class PolyWastageDetail(models.Model):
    damage = models.CharField(max_length=255, null=True)
    wrinkle = models.CharField(max_length=255, null=True)
    coreEnd = models.CharField(max_length=255, db_column='coreEnd', null=True)
 
 
class WorkOrderHeader(models.Model):
    workOrderNo = models.CharField(max_length=255, null=True)
    customer = models.CharField(max_length=255, null=True)
    jobName = models.CharField(max_length=255, db_column='jobName', null=True)
    sleeveSize = models.CharField(max_length=255, db_column='sleeveSize', null=True)
    target = models.CharField(max_length=255, null=True)
    produced = models.CharField(max_length=255, null=True)
    balance = models.CharField(max_length=255, null=True)
    operatorName = models.CharField(max_length=255, db_column='operatorName', null=True)
    assistantName = models.CharField(max_length=255, db_column='assistantName', null=True)
    date = models.CharField(max_length=255, null=True)
    mcName = models.CharField(max_length=255, db_column='mcName', null=True)
    shift = models.CharField(max_length=255, null=True)
    mcSpeed = models.CharField(max_length=255, null=True)
    productionWeight = models.CharField(max_length=255, null=True)
    dyanLevel = models.CharField(max_length=255, null=True)
    ProductionDetails = models.ManyToManyField(ProductionDetail, null=True)
    materialDetails = models.ManyToManyField(MaterialDetail, null=True)
    scrapDetails = models.OneToOneField(ScrapDetail, on_delete=models.CASCADE, null=True)
    machineParameters = models.OneToOneField(MachineParameter, on_delete=models.CASCADE, null=True)
    lineClearance = models.OneToOneField(LineClearance, on_delete=models.CASCADE, null=True)
    polyWastageDetails = models.OneToOneField(PolyWastageDetail, on_delete=models.CASCADE, null=True)
    breakDownDetail = models.OneToOneField(breakDownDetail, on_delete=models.CASCADE, null=True)