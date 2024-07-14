from django.urls import path
from . import views

urlpatterns = [
    # path('', views.apiOverview, name = "apiOverview"),
    path('tes', views.ShowTes, name = "tes"),
    # route customer
    path('customer', views.ShowCustomer, name = "get_customer"),
    path('customer/create', views.addCustomer, name = "add_customer"),
    
    #route product 
    path('product', views.showProduct, name = "get_product"),
]