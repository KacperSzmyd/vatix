from django.urls import path
from .views import AssigDeviceView, DeviceLocationView, UserLastLocalizationView

urlpatterns = [
    path("devices/<str:id>/assign", AssigDeviceView.as_view(), name="assign-device"),
    path(
        "devices/<str:id>/location",
        DeviceLocationView.as_view(),
        name="device-localization",
    ),
    path(
        "users/<int:id>/location",
        UserLastLocalizationView.as_view(),
        name="user-location",
    ),
]
