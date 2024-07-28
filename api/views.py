from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status
from rest_framework.decorators import api_view
from .controllers import Controllers
# from .serializers import ProductSerializer
# from .models import Product

# Create your views here.

@api_view(['GET'])
def ShowTes(request):
    return Response({'message' : 'Welcome to API Django Sales'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def ShowCustomer(request):
    return Controllers.customersget(request)

@api_view(['POST'])
def addCustomer(request):
    return Controllers.CreateAddCustomer(request)

@api_view(['GET'])
def showProduct(request):
    return Controllers.getProductDetail(request)

@api_view(['POST'])
def addSales(request):
    return Controllers.insertdatasale(request)

@api_view(['GET'])
def pagingView(request):
    return Controllers.pagingControllers(request)

@api_view(['GET'])
def compareView(request):
    return Controllers.comparedataControllers(request)

@api_view(['GET'])
def popularProductView(request):
    return Controllers.productPopuler(request)