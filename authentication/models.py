from django.db import models
from django.contrib.auth.models import AbstractUser
from pytz import country_names
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
import uuid


class Userall(models.TextChoices):
    CUSTOMER = 'customer'
    EMPLOYEE = 'employee'
    AGENT    = 'agency'
    OTHER    = 'other'


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    account_type = models.CharField(max_length=20,choices=Userall.choices,default='other',blank=True)
    is_approve = models.BooleanField(default=False)
    activation_email = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserPassword(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    password = models.CharField(max_length=55,blank=True)


class AgentInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    agency_name = models.CharField(max_length=100)
    agency_address = models.TextField(max_length=500)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    commission = models.CharField(max_length=100)
    type = models.CharField(max_length=50,choices=(('EQUINE','EQUINE'),('FARM','FARM')))
    date = models.DateField(auto_now=True)
    uploaded = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(f'{self.user} {self.type} Documents')


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    verified_equine = models.BooleanField(default=False)
    verified_farm = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100,blank=True)
    company_site = models.CharField(max_length=100,blank=True)
    phonenumber = models.CharField(max_length=100,blank=True)
    country_names = models.CharField(max_length=100,blank=True)
    communication = models.CharField(max_length=100,blank=True)
    occupation = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=100,blank=True)
    profile_img = models.ImageField(upload_to='profile/',blank=True)


    def __str__(self) -> str:
        return str(f'{self.user} Profile')
    

class AgentDocument(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True)
    document = models.FileField(upload_to='documents/',blank=True)

    def __str__(self) -> str:
        return str(f'{self.user} document')


class AgentLicense(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    state = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/',blank=True)

    def __str__(self) -> str:
        return str(f'{self.user} License')


class CustomPermission(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=300,blank=True)
 
 
class GroupPermission(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(CustomUser, related_name='userpermission')
    permision = models.ManyToManyField(CustomPermission, related_name='custompermission')