import pytest
from rest_framework.test import APIClient

from testing.factoryboy import (
    DriverFactory,
    OrderFactory,
    VehicleFactory,
)
from transport_management_core.models.order import Order, OrderStatusChoices

client = APIClient()
URL = "/api/orders/"


def create_fixtures(number: int = 2):
    for num in range(number):
        OrderFactory(driver=None, vehicle=None, order_number=f"order number {num}")


def test_orders_list(db):
    """Test GET at /api/orders/ 200"""

    create_fixtures()

    # let's have one order with assigned driver and vehicle to see the nested objects
    OrderFactory(
        driver=DriverFactory(),
        vehicle=VehicleFactory(),
        order_number="order number",
        status=OrderStatusChoices.IN_TRANSIT,
    )

    response = client.get(URL)
    assert response.status_code == 200
    response_json = response.json()

    # date_created is auto add now, so it spoils the tests
    for order in response_json:
        order.pop("date_created")
    assert response_json == [
        {
            "id": 1,
            "driver": None,
            "vehicle": None,
            "pickup_address": {
                "id": 1,
                "address": "",
                "x_coordinate": -1.0,
                "y_coordinate": -1.0,
            },
            "delivery_address": {
                "id": 2,
                "address": "",
                "x_coordinate": -1.0,
                "y_coordinate": -1.0,
            },
            "order_number": "order number 0",
            "customer_name": "",
            "weight": 12.3,
            "status": "new",
        },
        {
            "id": 2,
            "driver": None,
            "vehicle": None,
            "pickup_address": {
                "id": 3,
                "address": "",
                "x_coordinate": -1.0,
                "y_coordinate": -1.0,
            },
            "delivery_address": {
                "id": 4,
                "address": "",
                "x_coordinate": -1.0,
                "y_coordinate": -1.0,
            },
            "order_number": "order number 1",
            "customer_name": "",
            "weight": 12.3,
            "status": "new",
        },
        {
            "id": 3,
            "driver": {
                "id": 1,
                "name": "",
                "phone_number": "",
                "license_number": "",
                "is_available": True,
            },
            "vehicle": {
                "id": 1,
                "license_plate_number": "",
                "vehicle_type": "",
                "max_capacity": 123,
                "cost_per_km": 12.3,
                "is_available": True,
            },
            "pickup_address": {
                "id": 5,
                "address": "",
                "x_coordinate": -1.0,
                "y_coordinate": -1.0,
            },
            "delivery_address": {
                "id": 6,
                "address": "",
                "x_coordinate": -1.0,
                "y_coordinate": -1.0,
            },
            "order_number": "order number",
            "customer_name": "",
            "weight": 12.3,
            "status": "in transit",
        },
    ]


def test_orders_create_201(db):
    """Test POST at /api/orders/ 201"""

    data = {
        "order_number": "ecv",
        "customer_name": "Anicka Ancovicka",
        "pickup_address": {
            "address": "address 1",
            "x_coordinate": 100,
            "y_coordinate": 100,
        },
        "delivery_address": {
            "address": "address 2",
            "x_coordinate": 900,
            "y_coordinate": 900,
        },
        "weight": 12.3,
        # new orders don't have drivers and vehicles assigned by the logic
    }
    response = client.post(URL, data, format="json")
    assert response.status_code == 201
    response_json = response.json()
    response_json.pop("date_created")
    assert response_json == {
        "id": 1,
        "driver": None,
        "vehicle": None,
        "pickup_address": {
            "id": 1,
            "address": "address 1",
            "x_coordinate": 100.0,
            "y_coordinate": 100.0,
        },
        "delivery_address": {
            "id": 2,
            "address": "address 2",
            "x_coordinate": 900.0,
            "y_coordinate": 900.0,
        },
        "order_number": "ecv",
        "customer_name": "Anicka Ancovicka",
        "weight": 12.3,
        "status": "new",
    }


def test_orders_create_missing_fields(db):
    """Test POST at /api/orders/ 400"""

    data = {}
    response = client.post(URL, data)
    assert response.status_code == 400
    assert response.json() == {
        "order_number": ["This field is required."],
        "customer_name": ["This field is required."],
        "pickup_address": ["This field is required."],
        "delivery_address": ["This field is required."],
        "weight": ["This field is required."],
    }


def test_orders_create_same_addresses_400(db):
    """Test POST at /api/orders/ 400 - addresses are the same"""

    data = {
        "order_number": "ecv",
        "customer_name": "Anicka Ancovicka",
        "pickup_address": {
            "address": "address 1",
            "x_coordinate": 100,
            "y_coordinate": 100,
        },
        "delivery_address": {
            "address": "address 2",
            "x_coordinate": 100,
            "y_coordinate": 100,
        },
        "weight": 12.3,
        # new orders don't have drivers and vehicles assigned by the logic
    }
    response = client.post(URL, data, format="json")
    assert response.status_code == 400
    assert response.json() == {
        "non_field_errors": [
            "pickup and delivery address mut not have the same coordinates"
        ]
    }


def test_orders_detail_get_200(db):
    """Test GET at /api/orders/<id> 200"""

    order = OrderFactory()

    response = client.get(f"{URL}{order.pk}/")
    assert response.status_code == 200
    response_json = response.json()
    response_json.pop("date_created")
    assert response_json == {
        "id": 1,
        "driver": {
            "id": 1,
            "name": "",
            "phone_number": "",
            "license_number": "",
            "is_available": True,
        },
        "vehicle": {
            "id": 1,
            "license_plate_number": "",
            "vehicle_type": "",
            "max_capacity": 123,
            "cost_per_km": 12.3,
            "is_available": True,
        },
        "pickup_address": {
            "id": 1,
            "address": "",
            "x_coordinate": -1.0,
            "y_coordinate": -1.0,
        },
        "delivery_address": {
            "id": 2,
            "address": "",
            "x_coordinate": -1.0,
            "y_coordinate": -1.0,
        },
        "order_number": "",
        "customer_name": "",
        "weight": 12.3,
        "status": "new",
    }


def test_orders_detail_patch_200(db):
    """Test PATCH at /api/orders/<id> 200"""

    order = OrderFactory()

    data = {"order_number": "edited ON"}
    response = client.patch(f"{URL}{order.pk}/", data)
    assert response.status_code == 200
    response_json = response.json()
    response_json.pop("date_created")
    assert response_json == {
        "id": 1,
        "driver": {
            "id": 1,
            "name": "",
            "phone_number": "",
            "license_number": "",
            "is_available": True,
        },
        "vehicle": {
            "id": 1,
            "license_plate_number": "",
            "vehicle_type": "",
            "max_capacity": 123,
            "cost_per_km": 12.3,
            "is_available": True,
        },
        "pickup_address": {
            "id": 1,
            "address": "",
            "x_coordinate": -1.0,
            "y_coordinate": -1.0,
        },
        "delivery_address": {
            "id": 2,
            "address": "",
            "x_coordinate": -1.0,
            "y_coordinate": -1.0,
        },
        "order_number": "edited ON",
        "customer_name": "",
        "weight": 12.3,
        "status": "new",
    }


def test_orders_detail_patch_400_invalid_orders_type(db):
    """Test PATCH at /api/orders/<id> 200"""

    order = OrderFactory()

    data = {
        "order_number": "edited ON",
        "status": "sunbathing",
    }
    response = client.patch(f"{URL}{order.pk}/", data)
    assert response.status_code == 400
    assert response.json() == {"status": ['"sunbathing" is not a valid choice.']}


def test_orders_detail_delete_204(db):
    """Test DELETE at /api/orders/<id> 204"""

    order = OrderFactory()

    response = client.delete(f"{URL}{order.pk}/")
    assert response.status_code == 204

    with pytest.raises(Order.DoesNotExist):
        Order.objects.get(pk=order.pk)
