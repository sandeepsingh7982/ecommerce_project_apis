from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework.status import *
from .serializers import *
from products.serializers import ProductsSerializer
from products.models import Products
from .models import *
import jwt,datetime
import math

# Create your views here.

class Validate:
    def validate_user(self,request):
        try:
            token = request.COOKIES['']
            buyer_details = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms='HS256')
            buyer = Register.objects.get(id=buyer_details['id'], username = buyer_details['username'])
            if buyer:
                return buyer,True
            else:
                return "unauthorized",False 
        except:
            return "unauthorized",False
        
class RegisterView(GenericAPIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        buyer = Register.objects.filter(username=username,password=password).first()        
        serializer = RegisterSerializer(buyer)
        
        if buyer is None:
            return Response({'status':'Fail','message':'Buyer not found'}, status=HTTP_400_BAD_REQUEST)
        
        payload ={
        'id':buyer.id,
        'username':buyer.username,
        'exp':datetime.datetime.now() + datetime.timedelta(days=1)
        }
        auth_token = jwt.encode(payload,settings.JWT_SECRET_KEY)
        
        return Response({'message':'success','seller':serializer.data,'token':auth_token}, status=HTTP_200_OK)
        
        
        

class ProductView(GenericAPIView,Validate):
    def __init__(self):
        super().__init__()
        
    def get(self,request):
        buyer,st = self.validate_user(request)
        if st:
            page_num = int(request.data.get("page", 1))
            limit_num = int(request.data.get("limit", 10))
            start_num = (page_num - 1) * limit_num
            end_num = limit_num * page_num
            products = Products.objects.filter(qty__gte = 1)
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
        buyer,st = self.validate_user(request)
        if st:
            product_id = request.data.get('id')
            product_qty = request.data.get('qty')
            print(product_qty)
            product = Products.objects.get(id=product_id , qty__gte = product_qty)
            if product:
                product.qty = product.qty - int(product_qty)
                product.save()
                return Response({"status": "success", "message": "Buy successfully"}, status=HTTP_200_OK)
            return Response({"status": "fail", "message": 'product not found'}, status=HTTP_400_BAD_REQUEST)
        return Response({"status": "unauthrized", "message": "Invalid Seller"}, status=HTTP_400_BAD_REQUEST)
    
            
        
