from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from .serializers import ProductsSerializer
from .models import Products
from sellers.models import Register
import math
import datetime
import jwt
from django.conf import settings
from django.db.models import Q
import json

# Create your views here.

class Validate:
    def validate_user(self,request):
        try:
            token = request.COOKIES['']
            seller_details = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms='HS256')
            seller = Register.objects.get(id=seller_details['id'], username = seller_details['username'])
            if seller:
                return seller,True
            else:
                return "unauthorized",False 
        except:
            return "unauthorized",False
        
        

class ProductView(GenericAPIView,Validate):
    def __init__(self):
        super().__init__()
        
    def get(self,request):
        seller,st = self.validate_user(request)
        if st:
            product_id = request.data.get('id')
            if product_id:
                products = Products.objects.filter(Q(id = product_id) & Q(seller=seller))
                if len(products) == 0:
                    return Response({"status": "Fail", "message": "product not found"}, status=HTTP_400_BAD_REQUEST)
                serializer = ProductsSerializer(products,many=True)
                return Response({'status':'success','data':serializer.data},status=HTTP_200_OK)
            
            page_num = int(request.GET.get("page", 1))
            limit_num = int(request.GET.get("limit", 10))
            start_num = (page_num - 1) * limit_num
            end_num = limit_num * page_num
            products = Products.objects.filter(Q(seller=seller))
            total_products = products.count()
            serializer = ProductsSerializer(products[start_num:end_num],many=True)
            return Response({
                "status": "success",
                "total": total_products,
                "page": page_num,
                "last_page": math.ceil(total_products / limit_num),
                "data": serializer.data
            },status=HTTP_200_OK)
        return Response({"status": "unauthrized", "message": "Invalid Seller"}, status=HTTP_400_BAD_REQUEST)
        
    
    def post(self, request):
        seller,st = self.validate_user(request)
        if st:
            data = [{"product_name": request.data['product_name'],
                    "product_title": request.data['product_title'],
                    "product_category": request.data['product_category'],
                    "product_description": request.data['product_description'],
                    "price": request.data['price'],
                    "qty": request.data['qty'],'seller': seller.pk,'created_at' : datetime.datetime.now()}]
            serializer = ProductsSerializer(data=data,many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=HTTP_201_CREATED)
            return Response({"status": "fail", "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return Response({"status": "unauthrized", "message": "Invalid Seller"}, status=HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        seller,st = self.validate_user(request)
        if st:
            product_id = request.data['id']
            print(product_id)
            if product_id:
                product = Products.objects.get(id = product_id , seller=seller)
                serializer = ProductsSerializer(product,data=request.data,many=True)
                if serializer.is_valid():
                    serializer.validated_data['updated_at'] = datetime.datetime.now()
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data},status=HTTP_200_OK)
            
            return Response({"status": "success", "data": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return Response({"status": "unauthrized", "message": "Invalid Seller"}, status=HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        seller,st = self.validate_user(request)
        if st:
            product_id = request.data['id']
            if product_id:
                product = Products.objects.get(id = product_id , seller=seller)
                serializer = ProductsSerializer(product,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.validated_data['updated_at'] = datetime.datetime.now()
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data},status=HTTP_200_OK)
            
            return Response({"status": "success", "data": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return Response({"status": "unauthrized", "message": "Invalid Seller"}, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        seller,st = self.validate_user(request)
        if st:
            product_id = request.data.get('id',None)
            if product_id == None:
                return Response({"status": "fail", "message": "provide product id"}, status=HTTP_404_NOT_FOUND)

            product = Products.objects.filter(Q(id = product_id) & Q(seller=seller))
            if len(product) == 0:
                    return Response({"status": "Fail", "message": "product not found"}, status=HTTP_400_BAD_REQUEST)
            product.delete()
            return Response({"status": "success"},status=HTTP_204_NO_CONTENT)
        return Response({"status": "unauthrized", "message": "Invalid Seller"}, status=HTTP_400_BAD_REQUEST)
