from django.contrib.auth.models import User
from orderapp.models import Customer, Product
from rest_framework.authtoken.models import Token
from django.db import transaction
from orderapp.serializers import CustomerSerializer, ProductSerializer


def build_response(status, data):
    response = {
        'status': status,
        'data': data}
    return response


def initialise_customer(data):
    try:
        name = data.get('name')
        email = data.get('email')
        with transaction.atomic():
            customer = Customer.objects.filter(email=email).last()
            if customer:
                user = customer.user
            else:
                user = User.objects.create_user(username=email)
                customer = Customer.objects.create(name=name, email=email, user=user)
            token, created = Token.objects.get_or_create(user=user)
        return_data = {
            "token": token.key,
            "customer_id": customer.id
        }
        response = build_response(status='success', data=return_data)
        return response
    except Exception as exc:
        return_data = {"error": str(exc)}
        response = build_response(status='failure', data=return_data)
        return response


def view_customer(customer_id, data=None, only_view=False):
    status = 'success'
    status_code = 200
    customer = Customer.objects.filter(id=customer_id).last()
    if not customer:
        return_data = {
            "error": 'Invalid Customer ID, Customer Does not exist'
        }
        status = 'failure'
        status_code = 404
    else:
        if only_view:
            try:
                serializer = CustomerSerializer(customer)
                return_data = {
                    "customer": serializer.data
                }
            except Exception as exc:
                status = 'failure'
                return_data = {"error": str(exc)}
                status_code = 400
        else:
            try:
                serializer = CustomerSerializer(customer, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return_data = {
                        "customer": serializer.data
                    }
                else:
                    return_data = {
                        "error": serializer.errors
                    }
            except Exception as exc:
                status = 'failure'
                return_data = {"error": str(exc)}
                status_code = 400

    response = build_response(status, return_data)
    return response, status_code


def remove_customer(customer_id):
    customer = Customer.objects.filter(id=customer_id).last()
    if not customer:
        return_data = {
            "error": 'Invalid Customer ID, Customer Does not exist'
        }
        status = 'failure'
        status_code = 404
    else:
        customer.delete()
        return_data = {
            "message": 'This Customer has been removed from the Database Successfully'
        }
        status = 'success'
        status_code = 204

    response = build_response(status, return_data)
    return response, status_code


def create_product(data):
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return_data = {
            "product": serializer.data
        }
        status = 'success'
        status_code = 201
    else:
        return_data = {
            "error": serializer.errors
        }
        status = 'failure'
        status_code = 400

    response = build_response(status, return_data)
    return response, status_code


def get_product(product_id):
    product = Product.objects.filter(id=product_id).last()
    if not product:
        return_data = {
            "error": 'Invalid Product ID, Product Does not exist'
        }
        status = 'failure'
        status_code = 404
    else:
        try:
            serializer = ProductSerializer(product)
            return_data = {
                "product": serializer.data
            }
            status = 'success'
            status_code = 200
        except Exception as exc:
            status = 'failure'
            return_data = {"error": str(exc)}
            status_code = 400

    response = build_response(status, return_data)
    return response, status_code
