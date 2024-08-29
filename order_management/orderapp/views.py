from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from orderapp.models import Order
from orderapp.serializers import (
    CustomerInitSerializer, OrderSerializer, OrderOutSerializer
)
from orderapp.services import (
    initialise_customer,
    view_customer,
    remove_customer,
    create_product,
    get_product,
    build_response
)


class CreateCustomerView(APIView):
    def post(self, request):
        serializer = CustomerInitSerializer(data=request.data)
        if serializer.is_valid():
            response = initialise_customer(serializer.validated_data)
            if response['status'] == "success":
                status = 201
            else:
                status = 400
            return Response(response, status=status)
        else:
            return Response(serializer.errors, status=400)


class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        response, status = view_customer(customer_id, only_view=True)
        return Response(response, status=status)

    def put(self, request, customer_id):
        response, status = view_customer(customer_id, request.data)
        return Response(response, status=status)

    def delete(self, request, customer_id):
        response, status = remove_customer(customer_id, request.data)
        return Response(response, status=status)


class ProductCreateView(APIView):
    def post(self, request):
        response, status = create_product(request.data)
        return Response(response, status=status)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        response, status = get_product(product_id)
        return Response(response, status=status)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = serializer.save()
                order_serializer = OrderOutSerializer(order)
                return_data = {
                    "order": order_serializer.data
                }
                return Response(build_response('success', return_data), status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return_data = {
                    "error": str(e)
                }
                return Response(build_response('failure', return_data), status=status.HTTP_400_BAD_REQUEST)
        return_data = {
            "error": serializer.errors
        }
        return Response(build_response('failure', return_data), status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.filter(id=order_id).last()
        if not order:
            return_data = {
                "error": 'Invalid Order ID, Order Does not exist'
            }
            return Response(build_response('failure', return_data), status=status.HTTP_404_NOT_FOUND)
        serializer = OrderOutSerializer(order)
        return_data = {
            "order": serializer.data
        }
        return Response(build_response('success', return_data), status=200)
