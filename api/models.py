from django.db import models

# Create your models here.

class Customer(models.Model):
    customer_name = models.CharField(max_length=200, null = False, blank = False)
   
    def __str__(self):
        return self.customer_name
    
class Products(models.Model):
    product_code = models.CharField(max_length=15, null = True, blank = False)
    product_name = models.CharField(max_length=250, null = True, blank = False)
    product_price = models.FloatField(null = True, blank = True,)
    product_status = models.CharField(max_length=11, blank = False, default='0')
    product_stock = models.IntegerField( default=0)
    
    def __str__(self):
        return self.product_name

class Sales(models.Model):
    sale_date = models.DateTimeField(null=True, blank=True)
    sale_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    sale_items_total = models.IntegerField(default=0)
    
    def __str__(self):
        return f'Sales {self.id}'

class Sale_Items(models.Model):
    sale_id = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    product_price = models.FloatField(null = False, blank = False)
    item_qty = models.IntegerField(default=0)
    is_verify = models.IntegerField(default=0)

    
    def __str__(self):
        return f'Item {self.id} for Sale {self.sale_id.id}'