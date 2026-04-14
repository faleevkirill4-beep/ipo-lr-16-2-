# shop/admin.py
from django.contrib import admin
from .models import Category, Manufacturer, Product, Basket, BasketItem  # Новые имена

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'count', 'category', 'manufacturer']
    list_filter = ['category', 'manufacturer']
    search_fields = ['name', 'description']

@admin.register(Basket)  # Новое имя
class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    readonly_fields = ['created_at']

@admin.register(BasketItem)  # Новое имя
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'basket', 'product', 'count']  # basket вместо bascet