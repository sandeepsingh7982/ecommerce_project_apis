from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view() , name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('product', ProductView.as_view() , name='product')
]