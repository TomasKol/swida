import pytest

from testing.factoryboy import DriverFactory
from transport_management_core.models.driver import Driver

URL = "/api/drivers/"


def create_fixtures(number: int = 3):
    for num in range(number):
        DriverFactory(
            name=f"Driver Name {num}",
            phone_number=f"Phone number {num}",
            license_number=f"license_{num}",
            is_available=True,
        )


def test_driver_list(db, api_client):
    """Test GET at /api/drivers/ 200"""

    create_fixtures()

    response = api_client.get(URL)
    assert response.json() == [
        {
            "id": 1,
            "name": "Driver Name 0",
            "phone_number": "Phone number 0",
            "license_number": "license_0",
            "is_available": True,
        },
        {
            "id": 2,
            "name": "Driver Name 1",
            "phone_number": "Phone number 1",
            "license_number": "license_1",
            "is_available": True,
        },
        {
            "id": 3,
            "name": "Driver Name 2",
            "phone_number": "Phone number 2",
            "license_number": "license_2",
            "is_available": True,
        },
    ]


def test_driver_create_201(db, api_client):
    """Test POST at /api/drivers/ 201"""

    data = {
        "name": "Good Driver",
        "phone_number": "Phone number",
        "license_number": "license",
        "is_available": True,
    }
    response = api_client.post(URL, data)
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Good Driver",
        "phone_number": "Phone number",
        "license_number": "license",
        "is_available": True,
    }


def test_driver_create_missing_fields(db, api_client):
    """Test POST at /api/drivers/ 400"""

    data = {}
    response = api_client.post(URL, data)
    assert response.status_code == 400
    assert response.json() == {
        "name": ["This field is required."],
        "phone_number": ["This field is required."],
        "license_number": ["This field is required."],
    }


def test_driver_detail_get_200(db, api_client):
    """Test GET at /api/drivers/<id> 200"""

    driver = DriverFactory()

    response = api_client.get(f"{URL}{driver.pk}/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "",
        "phone_number": "",
        "license_number": "",
        "is_available": True,
    }


def test_driver_detail_patch_200(db, api_client):
    """Test PATCH at /api/drivers/<id> 200"""

    driver = DriverFactory()

    data = {"name": "edited name"}
    response = api_client.patch(f"{URL}{driver.pk}/", data)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "edited name",
        "phone_number": "",
        "license_number": "",
        "is_available": True,
    }


def test_driver_detail_delete_204(db, api_client):
    """Test DELETE at /api/drivers/<id> 204"""

    driver = DriverFactory()

    response = api_client.delete(f"{URL}{driver.pk}/")
    assert response.status_code == 204

    with pytest.raises(Driver.DoesNotExist):
        Driver.objects.get(pk=driver.pk)
