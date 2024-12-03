from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return self.create_user(email, username, first_name, password, **other_fields)
        
    def create_user(self, email, username, first_name, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    production_title = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    department = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=150, blank=True, null=True)

    productions = models.ManyToManyField('Production', related_name='users', blank=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username
    
    @property
    def production_titles(self):
        return ", ".join([production.production_title for production in self.productions.all()])

# Create your models here.
class Production(models.Model):
    create_date = models.DateField(auto_now_add=True)
    code = models.CharField(max_length=6, unique=True, null=True, blank=True)  # Add this field for the 6-digit code
    production_title = models.CharField(max_length=150, null=True) # Official or working title
    production_type = models.CharField(max_length=150, null=True) # Feature or TV
    production_studio = models.CharField(max_length=150, null=True)
    production_email = models.EmailField(_('email address'), null=True)
    production_address_1 = models.CharField(max_length=100, null=True, blank=True)
    production_address_2 = models.CharField(max_length=100, null=True, blank=True)
    production_city = models.CharField(max_length=100, null=True, blank=True)
    production_state = models.CharField(max_length=2, null=True, blank=True)
    production_zip = models.CharField(max_length=10, null=True, blank=True)
    production_phone = models.CharField(max_length=15, null=True, blank=True)
    purchase_order = models.CharField(max_length=10, null=True)
    coordinator_name = models.CharField(max_length=150, null=True)
    coordinator_email = models.EmailField(_('email address'), null=True)
    dot_admin_name = models.CharField(max_length=150, null=True)
    dot_admin_email = models.EmailField(_('email address'), null=True)
    captain_name = models.CharField(max_length=150, null=True)
    captain_email = models.EmailField(_('email address'), null=True)
    production_accountant_name = models.CharField(max_length=150, null=True, blank=True)
    production_accountant_email = models.EmailField(_('email address'), null=True, blank=True)
    production_accountant_phone = models.CharField(max_length=15, null=True, blank=True)
    production_supervisor_name = models.CharField(max_length=150, null=True, blank=True)
    production_supervisor_email = models.EmailField(_('email address'), null=True, blank=True)
    unit_production_manager_name = models.CharField(max_length=150, null=True, blank=True)
    unit_production_manager_email = models.EmailField(_('email address'), null=True, blank=True)
    first_shoot_day = models.DateField(null=True, blank=True)
    last_shoot_day = models.DateField(null=True, blank=True)
    total_shoot_days = models.IntegerField(null=True, blank=True)
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
    location_contact = models.CharField(max_length=15, blank=True)
    location_phone = models.CharField(max_length=15, blank=True)
    location_address_1 = models.CharField(max_length=100)
    location_address_2 = models.CharField(max_length=100, null=True, blank=True)
    location_city = models.CharField(max_length=100)
    location_state = models.CharField(max_length=2)
    location_zip = models.CharField(max_length=10)
    shoot_date = models.DateField(null=True, blank=True)
    shoot_day = models.IntegerField(null=True, blank=True)

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
    
class PurchaseOrders(models.Model):
    PO_TYPE_CHOICES = [
        ('', 'Select a PO Type'),
        ('Rental', 'Rental'),
        ('Purchase', 'Purchase'),
        ('Service', 'Service'),
        ('Other', 'Other'),
    ]

    create_date = models.DateField(auto_now_add=True)
    production_title = models.ForeignKey(Production, on_delete=models.CASCADE, null=True, blank=True)
    vendor_name = models.CharField(max_length=100)
    vendor_phone = models.CharField(max_length=15)
    vendor_contact = models.CharField(max_length=150, null=True, blank=True)
    vendor_address_1 = models.CharField(max_length=100)
    vendor_address_2 = models.CharField(max_length=100, null=True, blank=True)
    vendor_city = models.CharField(max_length=100)
    vendor_state = models.CharField(max_length=2)
    vendor_zip = models.CharField(max_length=10)
    po_number = models.CharField(max_length=10)
    po_date = models.DateField(null=True, blank=True)
    po_start_date = models.DateField(null=True, blank=True)
    po_end_date = models.DateField(null=True, blank=True)
    po_duration = models.IntegerField(null=True, blank=True)
    po_type = models.CharField(max_length=10, choices=PO_TYPE_CHOICES, null=True, blank=True)
    po_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    po_ammount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    po_subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    po_taxes = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    po_grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    po_description = models.TextField(max_length=2000, null=True, blank=True)
    is_budgeted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwards):
        self.po_grand_total = (self.po_subtotal or 0) + (self.po_taxes or 0)
        super().save(*args, **kwards)

    def __str__(self):
        return self.po_number
    
class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrders, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description