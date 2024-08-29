from django.urls import path
from orderapp import views


urlpatterns = [
    path('api/v1/customers/', views.CreateCustomerView.as_view(), name='create_customer'),
    path('api/v1/customers-detail/<int:customer_id>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('api/v1/products/', views.ProductCreateView.as_view(), name='create_product'),
    path('api/v1/products-detail/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('api/v1/orders/', views.OrderCreateView.as_view(), name='create_order'),
    path('api/v1/orders-detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
]