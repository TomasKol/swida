"""Modules for classes handling the inner business logic"""

from math import sqrt

import pandas as pd
from django.db.models import FloatField, OuterRef, QuerySet, Subquery

from transport_management_core.models import Driver, Order, Position, Vehicle


class OptimalVehicleFinder:
    """Handle finding the optimal vehicle for a given Order"""

    def __init__(self, order: Order):
        # assigned at init
        self.order: Order = order

        # assigned later during the process
        self.chosen_driver: Driver | None = None
        self.df: pd.DataFrame | None = None
        self.vehicles: QuerySet[Vehicle] | None = None
        self.result: dict[str, str | float] | None = None

        # run the logic on init so the result is available right after initialization
        self._run()

    def _run(self):
        """run the individual steps of the vehicle assignment"""

        self._get_vehicles()
        self._prepare_dataframe()
        self._perform_calculations()
        self._pick_driver()
        self._compose_result()

    def _compute_distance(self, row, destination):
        """Get distance between two points"""
        return sqrt(
            (row["x"] - destination.x_coordinate) ** 2
            + (row["y"] - destination.y_coordinate) ** 2
        )

    def _get_vehicles(self):
        """load all available vehicles with adequate capacity"""

        latest_position = Position.objects.filter(vehicle=OuterRef("pk")).order_by(
            "-timestamp"
        )
        vehicles = (
            Vehicle.objects.prefetch_related("position_set")
            .annotate(
                x=Subquery(
                    latest_position.values("x_coordinate")[:1],
                    output_field=FloatField(),
                ),
                y=Subquery(
                    latest_position.values("y_coordinate")[:1],
                    output_field=FloatField(),
                ),
            )
            .filter(
                is_available=True,
                max_capacity__gte=self.order.weight,
                x__isnull=False,
                y__isnull=False,
            )
        )

        # store in self to later feed it to dataframe creation
        self.vehicles = vehicles

    def _prepare_dataframe(self):
        """Prepare a pandas dataframe from the available Vehicles"""

        data = list(self.vehicles.values())
        self.df = pd.DataFrame(data)

    def _perform_calculations(self):
        """Calculate the distances and costs within the dataframe"""

        self.df["distance_to_pickup"] = self.df.apply(
            lambda row: self._compute_distance(row, self.order.pickup_address), axis=1
        )
        self.df["cost_of_pickup"] = (
            self.df["cost_per_km"] * self.df["distance_to_pickup"]
        )
        self.df["cost_of_transport"] = self.df["cost_per_km"] * self.order.distance
        self.df["total_cost"] = self.df["cost_of_pickup"] + self.df["cost_of_transport"]

        # sort the df by distance to pickup -> the winning vehicle will be the top row
        self.df.sort_values("distance_to_pickup", inplace=True)

    def _pick_driver(self):
        """Pick a driver for the job"""

        # I can't see any other logic to the driver selection other than being available
        self.chosen_driver = Driver.objects.filter(is_available=True).first()

    def _compose_result(self):
        """Compose the final outcome of the selection process"""

        top_row = self.df.iloc[0]
        distance_to_pickup = "{:.2f}".format(top_row["distance_to_pickup"])

        self.result = {
            "assigned_vehicle": top_row["license_plate_number"],
            "assigned_driver": self.chosen_driver.name,
            "estimated_cost_pickup": "{:.2f}".format(top_row["cost_of_pickup"]),
            "estimated_cost_total": "{:.2f}".format(top_row["total_cost"]),
            "distance_km": distance_to_pickup,
            "reasoning": f"Selected truck {top_row['license_plate_number']}: "
            f"closest available ({distance_to_pickup}km), "
            f"adequate capacity",
        }
