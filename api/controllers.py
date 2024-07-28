from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import CustomerSerializer, ProductsSerializer, SalesSerializer, SalesItemSerializer, SalesPagingSerializer
from .models import Customer, Products, Sales, Sale_Items
from django.db.models import Q, Sum, F
from datetime import datetime, timedelta

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
            return Response({"error": "Terjadi kesalahan Pada Server Pada Server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
            return Response({"error": "Terjadi kesalahan Pada Server Pada Server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
            return Response({"error": "Terjadi kesalahan Pada Server Pada Server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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

            if not sale_items:
                return Response({'message': 'Sale items list is required'}, status=status.HTTP_400_BAD_REQUEST)

            print("check sale_customer", sale_customer)
        
            sales_data = {
                'sale_date': sale_date,
                'sale_customer': sale_customer_id,
                'sale_items_total': len(sale_items) 
            }
            sales_serializer = SalesSerializer(data=sales_data)
            if sales_serializer.is_valid():
                sales_instance = sales_serializer.save()

                failed_items = []
                for item in sale_items:
                    product_id = item.get('product_id')
                    item_qty = item.get('item_qty')

                    product = Products.objects.get(id=product_id)

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
            return Response({"error": "Terjadi kesalahan Pada Server Pada Server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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

            sales = Sales.objects.filter(filters).annotate(
                total_price=Sum(F('sale_items__product_price') * F('sale_items__item_qty'))
            )
            
            total_data = sales.count()
            total_page = (total_data + total_data_show - 1) // total_data_show
            sales = sales[(page - 1) * total_data_show : page * total_data_show]

            sales_serializer = SalesPagingSerializer(sales, many=True)
            # print("check data sales", sales_serializer.data)
            
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
            return Response({"error": "Terjadi kesalahan Pada Server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    def comparedataControllers(request, format=None):
        try:
            keyword = request.GET.get('keyword', '')
            date_1 = request.GET.get('date_1', '')
            date_2 = request.GET.get('date_2', '')
            
            if not date_1 or not date_2:
                return Response({'message': 'Both date_1 and date_2 are required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                date_1_start = datetime.strptime(date_1, '%d/%m/%Y')
                date_2_start = datetime.strptime(date_2, '%d/%m/%Y')
                date_1_end = date_1_start + timedelta(days=1)
                date_2_end = date_2_start + timedelta(days=1)
            except ValueError:
                return Response({'message': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

            date_1_data = Sale_Items.objects.filter(
                sale_id__sale_date__range=(date_1_start, date_1_end)
            ).annotate(
                hour=F('sale_id__sale_date__hour')
            ).values(
                'hour'
            ).annotate(
                total=Sum(F('product_price') * F('item_qty'))
            ).order_by('hour')
            
            date_2_data = Sale_Items.objects.filter(
                sale_id__sale_date__range=(date_2_start, date_2_end)
            ).annotate(
                hour=F('sale_id__sale_date__hour')
            ).values(
                'hour'
            ).annotate(
                total=Sum(F('product_price') * F('item_qty'))
            ).order_by('hour')

            date_1_rows = [{'time': item['hour'], 'total': item['total']} for item in date_1_data]
            date_2_rows = [{'time': item['hour'], 'total': item['total']} for item in date_2_data]

            response_data = {
                "params": [
                    {
                        "date_1": date_1,
                        "date_2": date_2
                    }
                ],
                "data": [
                    {
                        "date_1_rows" : date_1_rows,
                        "date_2_rows" : date_2_rows,
                    }
                ]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Terjadi kesalahan Pada Server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    def productPopuler(request, format=None):
        try:
            periode_start = request.GET.get('data_periode_start', '')
            periode_end = request.GET.get('data_periode_end', '')
            total_data_show = int(request.GET.get('total_data_show', ''))
            
            if not periode_start or not periode_end:
                return Response({'message': 'Both periode_start and periode_end are required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                periode_start_date = datetime.strptime(periode_start, '%d/%m/%Y')
                periode_end_date = datetime.strptime(periode_end, '%d/%m/%Y')
            except ValueError:
                return Response({'message': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

            populer_product = Sale_Items.objects.filter(
                sale_id__sale_date__range=(periode_start_date, periode_end_date)
            ).values(
                'product_id'
            ).annotate(
                total_price=Sum(F('product_price') * F('item_qty')),
                total_items=Sum('item_qty')
            ).order_by('-total_price')[:total_data_show]
        
            product_data = []
            for item in populer_product:
                product = Products.objects.get(id=item['product_id'])
                product_data.append({
                    "Product_id" : product.id,
                    "Product_name" :  product.product_name,
                    "Product_price" : product.product_price,
                    "Total_items" : item['total_items'],
                    "Total_price" : item['total_price'],
                })
                

            response_data = {
                "params": [
                    {
                        "data_periode_start": periode_start,
                        "data_periode_end": periode_end,
                        "total_data_show": total_data_show
                    }
                ],
                "data": product_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)