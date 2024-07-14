from django.contrib import admin
from . models import Customer, Products, Sales, Sale_Items
# Register your models here.
admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Sales)
admin.site.register(Sale_Items)