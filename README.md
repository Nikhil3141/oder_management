# Order Management API

## API Specifications
##### API #1: POST /api/product/
```sh
URL : <hostname>/api/product/

Addition of new Product 

REQUEST BODY:

{
"product":"Apples",
"quantity":5
}

RESPONSE:

{
    "message": "SUCCESS",
    "status": 200,
    "data": "Item Added"
}
```


##### API #2: GET /api/product/
```sh
URL : <hostname>/api/product/

List all the Products

Query Params : page , size


RESPONSE:

{
    "message": "SUCCESS",
    "status": 200,
    "data": {
        "page_data": [
            {
                "id": 1,
                "product_name": "APPLE",
                "price": 0,
                "description": "",
                "quantity": 5
            }
        ],
        "total_pages": 1,
        "page": 1,
        "total_items": 1
    }
}
```

##### API #3: DELETE /api/product/
```sh
URL : <hostname>/api/product/

Delete the Product 

Query Params : product : Apple


RESPONSE:

{
    "message": "SUCCESS",
    "status": 200,
    "data": Product Deleted Successfully
}
```

##### API #4: PUT /api/product/
```sh
URL : <hostname>/api/product/

Editing Product 

REQUEST BODY:

{
"product_name":"APPLE",
"quantity":10
}

RESPONSE:

{
    "message": "SUCCESS",
    "status": 200,
    "data": "Item Updated"
}
```


##### API #5: POST /api/order/
```sh
URL : <hostname>/api/order/

Placing an Order 

REQUEST BODY:

{
"product_name":"APPLE",
"quantity":10
}

RESPONSE:
{
    "message": "SUCCESS",
    "status": 200,
    "data": "Order Placed Successfully"
}
```

Setting Up Enviroment :

Commands :

pipenv install --deploy - To install all packages from Pipfile

pipenv run python manage.py makemigrations

pipenv run python manage.py migrate

pipenv run python manage.py runserver 