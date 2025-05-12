from django.urls import path
from .views import (
    AssigDeviceView,
    DeviceLocationView,
    UserLastLocalizationView,
    MapView,
    UnassignDeviceView,
    DeviceListView,
)

urlpatterns = [
    path("devices/<str:id>/assign/", AssigDeviceView.as_view(), name="assign-device"),
    path(
        "devices/<str:id>/location/",
        DeviceLocationView.as_view(),
        name="device-localization",
    ),
    path(
        "users/<int:id>/location/",
        UserLastLocalizationView.as_view(),
        name="user-location",
    ),
    path("map/", MapView.as_view(), name="device-map"),
    path(
        "devices/<str:id>/unassign/",
        UnassignDeviceView.as_view(),
        name="unassign-device",
    ),
    path("devices/", DeviceListView.as_view(), name="device-list"),
]
