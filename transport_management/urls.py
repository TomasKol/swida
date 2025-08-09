"""URL configuration for transport_management project."""

from django.urls import include, path

urlpatterns = [
    path("api", include("transport_management_core.urls")),
]
