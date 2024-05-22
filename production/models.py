from django.db import models

# Create your models here.

class RadioScanner(models.Model):
    barcode = models.CharField(max_length=255)
    production = models.CharField(max_length=100)
    assigned_employee = models.CharField(max_length=100, null=True)
    assigned_department = models.CharField(max_length=100)
    scanned_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=1000)

    def __str__(self):
        return self.barcode
    

