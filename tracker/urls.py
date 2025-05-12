from django.urls import path
from .views import AssigDeviceView, DeviceLocalizationView

urlpatterns = [
    path("devices/<str:id>/assign", AssigDeviceView.as_view(), name="assign-device"),
    path(
        "devices/<str:id>/localization",
        DeviceLocalizationView.as_view(),
        name="device-localization",
    ),
]
