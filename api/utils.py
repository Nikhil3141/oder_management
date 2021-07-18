from rest_framework.status import *
from rest_framework.response import Response
import math, io
from django.core.files.base import ContentFile
from django.http import HttpResponse
import re,random,string
from .models import Product


def check_string(param):
    if str(param).strip() not in ['None', '', "", 'null']:
        return param
    return 'N.A.'


def check_int(param):
    try:
        param = int(param)
    except Exception as e:
        return 'N.A.'
    if param > 0:
        return param
    return 'N.A.'

def send_429(data):
    return update_response(message='ERROR', code=HTTP_429_TOO_MANY_REQUESTS, status=429, data=data)


def send_200(data):
    return update_response(message='SUCCESS', code=HTTP_200_OK, status=200, data=data)


def send_400(data):
    return update_response(message='ERROR', code=HTTP_400_BAD_REQUEST, status=400, data=data)


def send_401(data='You are not authorized for this action.'):
    return update_response(message='ERROR', code=HTTP_401_UNAUTHORIZED, status=401, data=data)


def send_500(data='Some exception occurred. Check the error log for details.'):
    return update_response(message='ERROR', code=HTTP_500_INTERNAL_SERVER_ERROR, status=500, data=data)


def send_no_auth(data='User not Logged In.'):
    return update_response(message='ERROR', code=HTTP_401_UNAUTHORIZED, status=401, data=data)


def update_response(message, code, **kwargs):
    resp_out = {}
    if (message is None):
        pass
    else:
        resp_out['message'] = message
    if kwargs is not None:
        for key, value in kwargs.items():
            resp_out[key] = value
    return Response(resp_out, status=code)


def check_page_and_size(page, size):
    try:
        page = int(page)
        size = int(size)
    except:
        pass
    if isinstance(page, int) and page >= 0:
        pass
    else:
        page = 1
    if isinstance(size, int) and size >= 0:
        pass
    else:
        size = 6
    return page, size


def check_empty_value(raw_body=None, **kwargs):
    if raw_body is not None:
        if raw_body == {} or raw_body == '':
            return 'KO! No data found in the body.'
    if kwargs is not None:
        for key, value in kwargs.items():
            if value is None or value == '':
                return 'KO! Empty Value. Provide value for: {0}. Found: {1}'.format(
                    key, value)
    else:
        return None


def paginate(li, page, size):
    try:
        page_number = int(page)
        page_size = int(size)
        if len(li):
            if page_size < 1 or page_number < 0:
                return []
            page_number = page_number - 1
            start_ind = 0 + page_size * page_number
            end_ind = start_ind + page_size

            total_pages = math.ceil(len(li) / page_size)

            return {"page_data": li[start_ind:end_ind], "size": page_size,
                    "total_pages": total_pages, "page": page_number + 1,
                    "total_items": len(li)}
        else:
            return {"page_data": [], "size": page_size, "page": page_number,
                    "total_pages": 0, "total_items": 0}

    except:
        return []

def get_history_match():
    return (
        Product.objects.filter(is_deleted=False).order_by('-created_at').values(
            "id",
            "product_name",
            "price",
            "quantity",
        )
    )


def create_unique_id():
    return ''.join(random.choices(string.digits, k=8))