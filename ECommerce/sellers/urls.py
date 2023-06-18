from django.urls import path,include
from .views import *

urlpatterns = [
    path('', include('products.urls')),
    path('register', RegisterView.as_view() , name='register'),
    path('login', LoginView.as_view(), name='login')
]