from django.contrib import admin
from .models import Category,Manufacturer,Bascet,Element_bascet,Product
# Register your models here.

admin.site.register(Category)
admin.site.register(Bascet)
admin.site.register(Element_bascet)
admin.site.register(Product)
admin.site.register(Manufacturer)