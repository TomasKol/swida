import pytest

from testing.factoryboy import PositionFactory, VehicleFactory
from transport_management_core.models.vehicle import Vehicle, VehicleTypeChoices

URL = "/api/vehicles/"


def create_fixtures(number: int = 3):
    for num in range(number):
        VehicleFactory(
            license_plate_number=f"ecv{num}",
            max_capacity=(num + 1) * 10,
            cost_per_km=num + 1,
            is_available=True,
        )


def test_vehicle_list(db, api_client):
    """Test GET at /api/vehicles/ 200"""

    create_fixtures()

    response = api_client.get(URL)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "license_plate_number": "ecv0",
            "vehicle_type": "",
            "max_capacity": 10,
            "cost_per_km": 1.0,
            "is_available": True,
        },
        {
            "id": 2,
            "license_plate_number": "ecv1",
            "vehicle_type": "",
            "max_capacity": 20,
            "cost_per_km": 2.0,
            "is_available": True,
        },
        {
            "id": 3,
            "license_plate_number": "ecv2",
            "vehicle_type": "",
            "max_capacity": 30,
            "cost_per_km": 3.0,
            "is_available": True,
        },
    ]


def test_vehicle_create_201(db, api_client):
    """Test POST at /api/vehicles/ 201"""

    data = {
        "license_plate_number": "ecv",
        "vehicle_type": VehicleTypeChoices.VAN,
        "max_capacity": 10,
        "cost_per_km": 1.0,
        "is_available": True,
    }
    response = api_client.post(URL, data)
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "license_plate_number": "ecv",
        "vehicle_type": "van",
        "max_capacity": 10,
        "cost_per_km": 1.0,
        "is_available": True,
    }


def test_vehicle_create_missing_fields(db, api_client):
    """Test POST at /api/vehicles/ 400"""

    data = {}
    response = api_client.post(URL, data)
    assert response.status_code == 400
    assert response.json() == {
        "license_plate_number": ["This field is required."],
        "vehicle_type": ["This field is required."],
        "max_capacity": ["This field is required."],
        "cost_per_km": ["This field is required."],
    }


def test_vehicle_detail_get_200(db, api_client):
    """Test GET at /api/vehicles/<id> 200"""

    vehicle = VehicleFactory()

    response = api_client.get(f"{URL}{vehicle.pk}/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "license_plate_number": "",
        "vehicle_type": "",
        "max_capacity": 123,
        "cost_per_km": 12.3,
        "is_available": True,
    }


def test_vehicle_detail_patch_200(db, api_client):
    """Test PATCH at /api/vehicles/<id> 200"""

    vehicle = VehicleFactory(vehicle_type=VehicleTypeChoices.VAN)

    data = {
        "license_plate_number": "edited ecv",
        "vehicle_type": VehicleTypeChoices.TRUCK,
    }
    response = api_client.patch(f"{URL}{vehicle.pk}/", data)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "license_plate_number": "edited ecv",
        "vehicle_type": "truck",
        "max_capacity": 123,
        "cost_per_km": 12.3,
        "is_available": True,
    }


def test_vehicle_detail_patch_400_invalid_vehicle_type(db, api_client):
    """Test PATCH at /api/vehicles/<id> 200"""

    vehicle = VehicleFactory(vehicle_type=VehicleTypeChoices.VAN)

    data = {
        "license_plate_number": "edited ecv",
        "vehicle_type": "wheelbarrow",
    }
    response = api_client.patch(f"{URL}{vehicle.pk}/", data)
    assert response.status_code == 400
    assert response.json() == {"vehicle_type": ['"wheelbarrow" is not a valid choice.']}


def test_vehicle_detail_delete_204(db, api_client):
    """Test DELETE at /api/vehicles/<id> 204"""

    vehicle = VehicleFactory()

    response = api_client.delete(f"{URL}{vehicle.pk}/")
    assert response.status_code == 204

    with pytest.raises(Vehicle.DoesNotExist):
        Vehicle.objects.get(pk=vehicle.pk)


def test_vehicle_current_position(db, api_client):
    """Test vehicle.current_position getter"""

    vehicle = VehicleFactory()
    for num in range(3):
        PositionFactory(vehicle=vehicle, x_coordinate=num, y_coordinate=num)

    latest_position = vehicle.position_set.order_by("-timestamp").first()

    assert vehicle.current_position.x_coordinate == latest_position.x_coordinate
    assert vehicle.current_position.y_coordinate == latest_position.y_coordinate
