from django.db import models

# Create your models here.

class Register(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name+self.last_name

    