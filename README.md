# Order Management API

A clean, production-ready Django REST Framework backend application designed for customer management, product inventory tracking, and order placement with automatic stock quantity validation. Originally built as a core backend practice application when preparing for senior backend interviews in early 2024, demonstrating solid architectural patterns, RESTful API design, and clean code standards.

---

## Key Features

* **Customer Management**: Initialize, view, update, and remove customer accounts integrated with Django's User authentication model.
* **Product Inventory Management**: Create and view products with stock quantity and price tracking.
* **Order Processing**: Place orders with nested product items, automatic stock quantity validation, and real-time inventory deduction.
* **Nested Serializers**: Structured JSON responses containing nested product details and computed order totals.
* **Modern Standards**: Django 4.2 & Python 3.11 compatibility, clean service-layer architecture, and explicit PEP8-compliant imports.

---

## Tech Stack

* **Framework**: Django 4.2 & Django REST Framework 3.18
* **Language**: Python 3.11
* **Database**: SQLite (Development)
* **Authentication**: DRF Token Authentication

---

## Repository Structure

```
order_management/
├── order_management/       # Django inner settings & configuration package
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── orderapp/               # Primary Django application
│   ├── models.py            # Database models (Customer, Product, Order, CartItem)
│   ├── serializers.py       # DRF Serializers & custom order validation
│   ├── services.py          # Business logic layer
│   ├── views.py             # API View controllers with IsAuthenticated rules
│   └── urls.py              # Endpoint routing
├── postman/                 # Postman collection for API testing
│   └── Order_Management.postman_collection.json
├── .gitignore               # Excludes virtual environments, db, and media files
├── manage.py                # Django command-line utility
└── requirements.txt         # Project dependencies
```

---

## Getting Started

### Prerequisites
* Python 3.11+
* Git

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:KiranAkshay2598/order_management.git
   cd order_management
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

The API will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/customers/` | Register/initialize customer account | No |
| `GET` | `/api/v1/customers-detail/<id>/` | View customer profile | Yes |
| `PUT` | `/api/v1/customers-detail/<id>/` | Update customer profile | Yes |
| `DELETE` | `/api/v1/customers-detail/<id>/` | Remove customer account | Yes |
| `POST` | `/api/v1/products/` | Create a new product entry | No |
| `GET` | `/api/v1/products-detail/<id>/` | View product details | Yes |
| `POST` | `/api/v1/orders/` | Place a new order with items | Yes |
| `GET` | `/api/v1/orders-detail/<id>/` | View order details and total price | Yes |

---

## Postman Collection

A pre-configured Postman collection is included in the `postman/` directory:
* File: `postman/Order_Management.postman_collection.json`

**To use**:
1. Open Postman.
2. Click **Import** and select `Order_Management.postman_collection.json`.
3. Set your `Authorization` header to `Token <your_token>` after creating a customer.
