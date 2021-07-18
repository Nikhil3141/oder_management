from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_create, name='product_create'),
    path('order/',views.order,name='order'),
]
