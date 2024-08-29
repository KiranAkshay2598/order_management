from rest_framework import serializers
from .models import Customer, Product, Order, CartItem


class CustomerInitSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock_quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        customer = validated_data['customer']
        order = Order.objects.create(customer=customer)
        for item_data in products_data:
            product = item_data['product']
            quantity = item_data['quantity']
            product_instance = Product.objects.get(id=product.id)
            if product_instance.stock_quantity < quantity:
                raise serializers.ValidationError('Insufficient product quantity')
            cart_item = CartItem.objects.filter(order=order, product=product_instance, quantity=quantity).last()
            if cart_item:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                CartItem.objects.create(order=order, product=product_instance, quantity=quantity)
        return order


class CartItemOutSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Nested serializer to include product details

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'total_price']


class OrderOutSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(source='cartitem_set', many=True)  # Use the related manager for CartItem

    class Meta:
        model = Order
        fields = ['id', 'customer', 'products', 'total_price']  # Include relevant fields

    def get_total_price(self, obj):
        return obj.total_price()
