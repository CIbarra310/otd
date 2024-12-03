from import_export import resources
from .models import Production, Vendor, Location, Department, JobTitle, PurchaseOrders

class ProductionResource(resources.ModelResource):
    class Meta:
        model = Production

class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendor

class LocationResource(resources.ModelResource):
    class Meta:
        model = Location

class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department

class JobTitleResource(resources.ModelResource):
    class Meta:
        model = JobTitle

class PurchaseOrderResource(resources.ModelResource):
    class Meta:
        model = PurchaseOrders