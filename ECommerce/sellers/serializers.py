from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
   class Meta:
      model = Register
      fields = '__all__'