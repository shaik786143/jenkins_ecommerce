import pytest
from rest_framework.test import APIClient
from testapp.models import Product

@pytest.mark.django_db
def test_product_list_api():
    """
    Test that the product list API endpoint returns a successful response.
    """
    Product.objects.create(name="Test Product 1", price=10.00, inventory=100)
    Product.objects.create(name="Test Product 2", price=20.00, inventory=50)

    client = APIClient()
    response = client.get("/api/products/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Test Product 2" # Sorted by -created_at

@pytest.mark.django_db
def test_product_create_api():
    """
    Test that a product can be created via the API.
    """
    client = APIClient()
    product_data = {
        "name": "New Awesome Product",
        "description": "A truly awesome product.",
        "price": "99.99",
        "inventory": 25
    }
    response = client.post("/api/products/", product_data, format="json")

    assert response.status_code == 201
    assert Product.objects.count() == 1
    assert Product.objects.get().name == "New Awesome Product"
