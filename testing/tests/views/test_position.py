from rest_framework.test import APIClient

from testing.factoryboy import VehicleFactory

client = APIClient()
URL = "/api/positions/"


def create_fixtures(number: int = 3):
    for num in range(number):
        VehicleFactory(
            license_plate_number=f"ecv{num}",
            max_capacity=(num + 1) * 10,
            cost_per_km=num + 1,
            is_available=True,
        )


def test_position_create_201(db):
    """Test POST at /api/positions/ 201"""
    data = {
        "x_coordinate": 123,
        "y_coordinate": 123,
        "vehicle": VehicleFactory().pk,
    }
    response = client.post(URL, data)
    assert response.status_code == 201

    # timestamps are dynamic, out they go
    response_json = response.json()
    response_json.pop("timestamp")
    assert response_json == {
        "id": 1,
        "x_coordinate": 123.0,
        "y_coordinate": 123.0,
        "vehicle": 1,
    }


def test_position_create_400_missing_fields(db):
    """Test POST at /api/positions/ 400 - missing fields"""
    data = {}
    response = client.post(URL, data)
    assert response.status_code == 400
    assert response.json() == {
        "x_coordinate": ["This field is required."],
        "y_coordinate": ["This field is required."],
        "vehicle": ["This field is required."],
    }
