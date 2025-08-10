from testing.factoryboy import (
    AddressFactory,
    DriverFactory,
    OrderFactory,
    PositionFactory,
    VehicleFactory,
)
from transport_management_core.handlers import OptimalVehicleFinder


def test_optimal_vehicle_finder_1(db):
    """Test OptimalVehicleFinder - the easiest case"""

    # set up data
    DriverFactory(name="Driver 1", license_number="License 1", is_available=True)
    order = OrderFactory(
        weight=10,
        pickup_address=AddressFactory(x_coordinate=0, y_coordinate=0),
        delivery_address=AddressFactory(x_coordinate=100, y_coordinate=100),
    )

    vehicle_1 = VehicleFactory(
        license_plate_number="Vehicle 1",
        max_capacity=100,
        is_available=True,
        cost_per_km=5,
    )
    PositionFactory(x_coordinate=10, y_coordinate=10, vehicle=vehicle_1)

    # run and test finder
    finder = OptimalVehicleFinder(order)
    result = finder.result
    assert result == {
        "assigned_vehicle": "Vehicle 1",
        "assigned_driver": "Driver 1",
        "estimated_cost_pickup": "70.71",
        "estimated_cost_total": "777.82",
        "distance_km": "14.14",
        "reasoning": "Selected truck Vehicle 1: closest available (14.14km), adequate capacity",
    }


def test_optimal_vehicle_finder_2(db):
    """Test OptimalVehicleFinder - with unavailable vehicle closer to pickup place"""

    # set up data
    DriverFactory(name="Driver 1", license_number="License 1", is_available=True)
    order = OrderFactory(
        weight=10,
        pickup_address=AddressFactory(x_coordinate=0, y_coordinate=0),
        delivery_address=AddressFactory(x_coordinate=100, y_coordinate=100),
    )

    vehicle_1 = VehicleFactory(
        license_plate_number="Vehicle 1",
        max_capacity=100,
        is_available=True,
        cost_per_km=5,
    )
    PositionFactory(x_coordinate=10, y_coordinate=10, vehicle=vehicle_1)

    vehicle_unavailable = VehicleFactory(
        license_plate_number="Vehicle 2",
        max_capacity=100,
        is_available=False,
        cost_per_km=5,
    )
    PositionFactory(x_coordinate=5, y_coordinate=5, vehicle=vehicle_unavailable)

    # run and test finder
    finder = OptimalVehicleFinder(order)
    result = finder.result
    assert result == {
        "assigned_vehicle": "Vehicle 1",
        "assigned_driver": "Driver 1",
        "estimated_cost_pickup": "70.71",
        "estimated_cost_total": "777.82",
        "distance_km": "14.14",
        "reasoning": "Selected truck Vehicle 1: closest available (14.14km), adequate capacity",
    }


def test_optimal_vehicle_finder_3(db):
    """Test OptimalVehicleFinder - with vehicle with insufficient capacity closer to pickup place"""

    # set up data
    DriverFactory(name="Driver 1", license_number="License 1", is_available=True)
    order = OrderFactory(
        weight=10,
        pickup_address=AddressFactory(x_coordinate=0, y_coordinate=0),
        delivery_address=AddressFactory(x_coordinate=100, y_coordinate=100),
    )

    vehicle_1 = VehicleFactory(
        license_plate_number="Vehicle 1",
        max_capacity=100,
        is_available=True,
        cost_per_km=5,
    )
    PositionFactory(x_coordinate=10, y_coordinate=10, vehicle=vehicle_1)

    vehicle_small = VehicleFactory(
        license_plate_number="Vehicle 2",
        max_capacity=1,
        is_available=True,
        cost_per_km=5,
    )
    PositionFactory(x_coordinate=5, y_coordinate=5, vehicle=vehicle_small)

    # run and test finder
    finder = OptimalVehicleFinder(order)
    result = finder.result
    assert result == {
        "assigned_vehicle": "Vehicle 1",
        "assigned_driver": "Driver 1",
        "estimated_cost_pickup": "70.71",
        "estimated_cost_total": "777.82",
        "distance_km": "14.14",
        "reasoning": "Selected truck Vehicle 1: closest available (14.14km), adequate capacity",
    }


def test_optimal_vehicle_finder_4(db):
    """Test OptimalVehicleFinder - choose closer vehicle"""

    # set up data
    DriverFactory(name="Driver 1", license_number="License 1", is_available=True)
    order = OrderFactory(
        weight=10,
        pickup_address=AddressFactory(x_coordinate=0, y_coordinate=0),
        delivery_address=AddressFactory(x_coordinate=100, y_coordinate=100),
    )

    vehicle_1 = VehicleFactory(
        license_plate_number="Vehicle 1",
        max_capacity=100,
        is_available=True,
        cost_per_km=5,
    )
    PositionFactory(x_coordinate=10, y_coordinate=10, vehicle=vehicle_1)

    vehicle_2 = VehicleFactory(
        license_plate_number="Vehicle 2",
        max_capacity=100,
        is_available=True,
        cost_per_km=5,
    )
    PositionFactory(x_coordinate=50, y_coordinate=50, vehicle=vehicle_2)

    # run and test finder
    finder = OptimalVehicleFinder(order)
    result = finder.result
    assert result == {
        "assigned_vehicle": "Vehicle 1",
        "assigned_driver": "Driver 1",
        "estimated_cost_pickup": "70.71",
        "estimated_cost_total": "777.82",
        "distance_km": "14.14",
        "reasoning": "Selected truck Vehicle 1: closest available (14.14km), adequate capacity",
    }
