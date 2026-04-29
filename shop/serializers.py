from rest_framework import serializers
from .models import Product,Category,Manufacturer,Basket,BasketItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'
    

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Manufacturer
        fields = '__all__'


class BasketSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Basket
        fields = '__all__'


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BasketItem
        fields = '__all__'

    