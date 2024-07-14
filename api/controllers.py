from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import CustomerSerializer, ProductsSerializer
from .models import Customer, Products

class Controllers:
    
    @staticmethod
    def customersget(request):
        try:
            ids = request.GET.getlist('ids')
            keyword = request.GET.get('keyword', '')
            
            customers = Customer.objects.all()
            if not customers:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            if ids and ids != ['']:
                customers = Customer.objects.filter(id__in=ids)
            elif keyword:
                customers = Customer.objects.filter(customer_name__icontains=keyword)
            
            serializer = CustomerSerializer(customers, many=True)
            response_data = {
                "ids": ids,
                "keyword": keyword,
                "total": customers.count(),
                "status": status.HTTP_200_OK,
                "rows": serializer.data
            }
            return Response(response_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def CreateAddCustomer(request):
        try:
            customer_name = request.data.get('customer', '')
            
            serializer = CustomerSerializer(data={'customer_name': customer_name})
            print("data Serializer", serializer)
            if serializer.is_valid():
                serializer.save()
                return Response({'messagetype' : 'S', 'message' : 'create Product Successfully', 'data' :serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'messagetype' : 'E', 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'messagetype' : 'E', 'message':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def getProductDetail(request):
        try:
            product_code = request.GET.get('code', '')
            print("check product_code", product_code)
            if not product_code:
                return Response({"error": "Product code parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            product = Products.objects.filter(product_code=product_code).first()
            print("check Product", product)
            if not product:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            if product.product_status == "hold":
                return Response({"message": "Product is on hold"}, status=status.HTTP_400_BAD_REQUEST)

            if product.product_stock == 0:
                return Response({"message": "Product is out of stock"}, status=status.HTTP_400_BAD_REQUEST)

            # serializer = ProductsSerializer(product)
            response_data = {
                "code": product_code,
                "status": status.HTTP_200_OK,
                "data": [{
                    "id": product.id,
                    "name": product.product_name,
                    "price": product.product_price
                }]
            }
            return Response(response_data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)