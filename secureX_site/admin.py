from django.contrib import admin
from secureX_site.models import RequestService
from secureX_site.models import Service,OpenJob,JobApplication,BranchLocation,Profile,Course,OrderItem,Order,DeliveryAdd
# Register your models here.
admin.site.register(RequestService)
admin.site.register(Service)
admin.site.register(OpenJob)
admin.site.register(JobApplication)
admin.site.register(BranchLocation)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryAdd)
