from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import CustomerSerializer, ProductsSerializer, SalesSerializer, SalesItemSerializer
from .models import Customer, Products, Sales, Sale_Items
from django.db.models import Q
from datetime import datetime

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
        
    @staticmethod
    def insertdatasale(request):
        try:
            sale_date = request.data.get('sale_date', None)
            sale_customer_id = request.data.get('sale_customer', None)
            sale_items = request.data.get('sale_items', None)

            # Validate sale_customer_id
            if sale_customer_id is None:
                return Response({'message': 'Sale customer ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                sale_customer = Customer.objects.get(id=sale_customer_id)
            except Customer.DoesNotExist:
                return Response({'message': 'Invalid sale customer ID'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate sale_items
            if not sale_items:
                return Response({'message': 'Sale items list is required'}, status=status.HTTP_400_BAD_REQUEST)

            print("check sale_customer", sale_customer)
            # Create Sales instance
            sales_data = {
                'sale_date': sale_date,
                'sale_customer': sale_customer_id,
                'sale_items_total': len(sale_items)  # Assuming sale_items_total is the count of items
            }
            sales_serializer = SalesSerializer(data=sales_data)
            if sales_serializer.is_valid():
                sales_instance = sales_serializer.save()

                # Process sale items
                failed_items = []
                for item in sale_items:
                    product_id = item.get('product_id')
                    item_qty = item.get('item_qty')

                    # Fetch product instance
                    product = Products.objects.get(id=product_id)

                    # Validate quantity
                    if item_qty > product.product_stock:
                        failed_items.append({
                            'product_id': product_id,
                            'message': 'Quantity exceeds available stock'
                        })
                    else:
              
                        sale_item_data = {
                            'sale_id': sales_instance.id,
                            'product_id': product_id,
                            'product_price': product.product_price,
                            'item_qty': item_qty,
                            'is_verify': 0  
                        }
                        sale_item_serializer = SalesItemSerializer(data=sale_item_data)
                        if sale_item_serializer.is_valid():
                            sale_item_serializer.save()

                            product.product_stock -= item_qty
                            product.save()

                if failed_items:
                    return Response({
                        'message': 'Some items failed to insert',
                        'failed_items': failed_items
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        'message': 'Sales and sale items inserted successfully',
                        'data': {
                            'sales': sales_serializer.data,
                            'sale_items': SalesItemSerializer(sales_instance.sale_items.all(), many=True).data
                        }
                    }, status=status.HTTP_201_CREATED)

            return Response(sales_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("check error", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    def pagingControllers(request, format=None):
        try:
            keyword = request.GET.get('keyword', '')
            data_periode_start = request.GET.get('data_periode_start', '')
            data_periode_end = request.GET.get('data_periode_end', '')
            total_data_show = int(request.GET.get('total_data_show', 10))
            page = int(request.GET.get('page', 1))

            filters = Q()
            
            if keyword:
                filters &= Q(id__icontains=keyword) | Q(sale_customer__customer_name__icontains=keyword)
            
            if data_periode_start and data_periode_end:
                try:
                    data_periode_start_date = datetime.strptime(data_periode_start, '%d/%m/%Y')
                    data_periode_end_date = datetime.strptime(data_periode_end, '%d/%m/%Y')
                    filters &= Q(sale_date__range=(data_periode_start_date, data_periode_end_date))
                except ValueError:
                    return Response({'message': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

            sales = Sales.objects.filter(filters)
            total_data = sales.count()
            total_page = (total_data + total_data_show - 1) // total_data_show
            sales = sales[(page - 1) * total_data_show : page * total_data_show]

            sales_serializer = SalesSerializer(sales, many=True)
            response_data = {
                "params": [
                    {
                        "keyword": keyword,
                        "data_periode_start": data_periode_start,
                        "data_periode_end": data_periode_end,
                        "total_data_show": total_data_show
                    }
                ],
                "data": [
                    {
                        "keyword": keyword,
                        "total_data": total_data,
                        "total_data_show": total_data_show,
                        "total_page": total_page,
                        "Page": page,
                        "status": 200,
                        "rows": sales_serializer.data
                    }
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)