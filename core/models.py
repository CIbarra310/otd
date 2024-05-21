from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return self.create_user(email, user_name, first_name, password, **other_fields)
        
    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    production_title = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    department = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name

# Create your models here.
class Production(models.Model):
    create_date = models.DateField(auto_now_add=True)
    production_title = models.CharField(max_length=150, null=True)
    production_studio = models.CharField(max_length=150, null=True)
    production_email = models.EmailField(_('email address'), null=True)
    purchase_order = models.CharField(max_length=10, null=True)
    coordinator_name = models.CharField(max_length=150, null=True)
    coordinator_email = models.EmailField(_('email address'), null=True)
    captain_name = models.CharField(max_length=150, null=True)
    captain_email = models.EmailField(_('email address'), null=True)
    production_notes = models.TextField(max_length=2000, null=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.production_title

class Vendor(models.Model):
    create_date = models.DateField(auto_now_add=True)
    vendor_name = models.CharField(max_length=100)
    vendor_phone = models.CharField(max_length=15)
    vendor_address_1 = models.CharField(max_length=100)
    vendor_address_2 = models.CharField(max_length=100, null=True, blank=True)
    vendor_city = models.CharField(max_length=100)
    vendor_state = models.CharField(max_length=2)
    vendor_zip = models.CharField(max_length=10)
    
    def __str__(self):
        return self.vendor_name

class Location(models.Model):
    production_title = models.CharField(max_length=150, null=True)
    location_name = models.CharField(max_length=100)
    location_contact = models.CharField(max_length=15)
    location_address_1 = models.CharField(max_length=100)
    location_address_2 = models.CharField(max_length=100, null=True)
    location_city = models.CharField(max_length=100)
    location_state = models.CharField(max_length=2)
    location_zip = models.CharField(max_length=10) 

    def __str__(self):
        return self.location_name
    
class Department(models.Model):
    department_title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.department_title

class JobTitle(models.Model):
    department_title = models.ForeignKey(Department, on_delete=models.CASCADE, default='')
    job_title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.job_title}"