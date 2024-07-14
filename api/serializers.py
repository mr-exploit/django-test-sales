from rest_framework import serializers
from .models import Customer, Products, Sales, Sale_Items

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Customer is required.")
        return value
    
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

    def validate_product_name(self, value):
        if not value:
            raise serializers.ValidationError("Product name is required.")
        return value
    
class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Sales is required.")
        return value
    
class SalesItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale_Items
        fields = '__all__'

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Sales is required.")
        return value