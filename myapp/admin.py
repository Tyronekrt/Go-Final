from faulthandler import register

from django.contrib import admin

# Register your models here.
from myapp.models import Member, Product, Appointment, Contact, User, ImageModel

admin.site.register(Member)
admin.site.register(Product)
admin.site.register(Appointment)
admin.site.register(Contact)
admin.site.register(User)
admin.site.register(ImageModel)
