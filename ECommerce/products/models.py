from django.db import models
from sellers.models import Register
# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=50, null=True)
    product_title = models.CharField(max_length=50, null=True)
    product_category = models.CharField(max_length=50, null=True)
    product_description = models.TextField(null=True)
    price = models.IntegerField(null=True)
    qty = models.IntegerField(null=True)
    seller = models.ForeignKey(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']