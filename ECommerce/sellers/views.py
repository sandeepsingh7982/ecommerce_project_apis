from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework.status import *
from .serializers import *
from .models import *
import jwt,datetime

# Create your views here.

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
        
        seller = Register.objects.filter(username=username,password=password).first()
        
        serializer = RegisterSerializer(seller)
        
        if seller is None:
            return Response({'status':'Fail','message':'Seller not found'}, status=HTTP_400_BAD_REQUEST)
        
        payload ={
            'id':seller.id,
            'username':seller.username,
            'exp':datetime.datetime.now() + datetime.timedelta(days=1)
        }
        auth_token = jwt.encode(payload,settings.JWT_SECRET_KEY)
        
        return Response({'message':'success','seller':serializer.data,'token':auth_token}, status=HTTP_200_OK)
            
            
        
