from rest_framework import serializers
from .models import Customer, Products, Sales, Sale_Items
from datetime import datetime

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

class DateFieldWithTimezone(serializers.DateField):
    def to_representation(self, value):
        if isinstance(value, datetime):
            value = value.date()
        return super(DateFieldWithTimezone, self).to_representation(value)
    
class SalesPagingSerializer(serializers.ModelSerializer):
    sale_code = serializers.CharField(source='id')
    sale_date = DateFieldWithTimezone(format="%d/%m/%Y")
    customer = serializers.CharField(source='sale_customer.customer_name')
    total_item = serializers.IntegerField(source='sale_items_total')
    total_price = serializers.IntegerField()

    class Meta:
        model = Sales
        fields = ['sale_code', 'sale_date', 'customer', 'total_item', 'total_price']
        
class TimeTotalSerializer(serializers.Serializer):
    time = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)

class ComparisonSerializer(serializers.Serializer):
    date_1_rows = TimeTotalSerializer(many=True)
    date_2_rows = TimeTotalSerializer(many=True)
    
        
class SalesItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale_Items
        fields = '__all__'

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Sales is required.")
        return value