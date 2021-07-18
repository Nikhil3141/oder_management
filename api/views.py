from rest_framework.response import Response
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import logging, traceback, sys
from rest_framework.status import *
from django.conf import settings
from django.shortcuts import render
from .models import Product, Order
from .utils import send_400, send_200, send_500, check_page_and_size, get_history_match, paginate, create_unique_id
from datetime import datetime


@api_view(["POST", "DELETE", "GET", "PUT"])
def product_create(request):
    if request.method == "POST":  ## To Add new Product into Database
        try:
            product = request.data.get('product')
            quantity = int(request.data.get('quantity'))
            if product is None:
                return send_400(data='Product is Empty')
            if quantity is None:
                return send_400(data='Quantity is Empty')
            if quantity <= 0:
                return send_400(data=f'Quantity Cannot be {quantity}')
            if Product.objects.filter(product_name=product, is_deleted=False).exists():
                return send_400(data='Product Already Exist')
            new_product = Product.objects.create(product_name=product, quantity=quantity)
            return send_200(data="Item Added")
        except:
            return send_500("Internal Error")
    if request.method == "DELETE":  ## To Delete Product from Database
        try:
            product_name = request.query_params.get("product")
            if product_name is None:
                return send_400(data='Product Name is Empty')
            if not Product.objects.filter(product_name=product_name, is_deleted=False).exists():
                return send_400(data='Invalid Product Name')
            tem_data = Product.objects.get(product_name=product_name, is_deleted=False)
            tem_data.is_deleted = True
            tem_data.deleted_at = datetime.now()
            tem_data.save(update_fields=['is_deleted', 'deleted_at'])
            return send_200(data="Product Deleted Successfully")
        except:
            return send_500("Internal Error")
    if request.method == "GET":  ## To show all the Product List
        try:
            page = request.query_params.get('page')
            size = request.query_params.get('size')
            page, size = check_page_and_size(page=page, size=size)
            data = get_history_match()
            data = paginate(data, page, size)
            return send_200(data=data)
        except Exception as e:
            return Response({"success": False, "message": "Some Exception occurred."}, status=500)
    if request.method == "PUT":  # To Update the elememt in a Product
        try:
            product_name = request.data.get('product_name')
            quantity = int(request.data.get("quantity"))
            if quantity <= 0:
                return send_400(data=f'Quantity Cannot be {quantity}')
            if not Product.objects.filter(product_name=product_name, is_deleted=False).exists():
                return send_400(data='Invalid Product ID')
            if product_name:
                tem_data = Product.objects.get(product_name=product_name, is_deleted=False)
                tem_data.product_name = product_name
                tem_data.save(update_fields=['product_name'])
            if quantity:
                tem_data = Product.objects.get(product_name=product_name, is_deleted=False)
                tem_data.quantity = quantity
                tem_data.save(update_fields=['quantity'])
            return send_200(data="Item Updated")
        except:
            return send_500("Internal Error")


@api_view(["POST"])
def order(request):  ## To Place an Order
    try:
        product = request.data.get('product')
        quantity = int(request.data.get('quantity'))
        if product is None:
            return send_400(data='Product is Empty')
        if quantity is None:
            return send_400(data='Quantity is Empty')
        if quantity <= 0:
            return send_400(data=f'Quantity Cannot be {quantity}')
        if Product.objects.filter(product_name=product, is_deleted=False).exists():
            tem_data = Product.objects.get(product_name=product, is_deleted=False)
            tem_data_quantity = tem_data.quantity
            if quantity <= tem_data_quantity:
                order_quantity = tem_data_quantity - quantity
                tem_data.quantity = order_quantity
                tem_data.save(update_fields=['quantity'])
                transcation = create_unique_id()
                Order.objects.create(product_name=product, quantity=quantity, transaction_id=transcation)
            else:
                return send_400(data=f'The Given Quantity {quantity} exceeds available Quantity {tem_data_quantity}')
        else:
            return send_400(data='Product does not exist')
        return send_200(data="Order Placed Successfully")
    except:
        return send_500("Internal Error")
