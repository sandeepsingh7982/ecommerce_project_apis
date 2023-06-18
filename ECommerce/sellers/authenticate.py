from rest_framework import authentication,exceptions
from django.conf import settings
import jwt,datetime
from .models import Register

class JWTAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        prefix,token = auth_data.decode('utf-8').split(' ')
        
        try:
            payload = jwt.decode(token,settings.JWT_SECRET_KEY)
            seller = Register.objects.get(username=payload['username'],password=payload['password'])
            return (seller,token)
        
        except jwt.DecodeError as error:
            raise exceptions.AuthenticationFailed('Your token is invalid')
        except jwt.ExpiredSignatureError as error:
            raise exceptions.AuthenticationFailed('Your token is expired')
        
