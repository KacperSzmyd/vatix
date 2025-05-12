from django.urls import path
from .views import AssigDeviceView, DeviceLocalizationView, UserLastLocalizationView

urlpatterns = [
    path("devices/<str:id>/assign/", AssigDeviceView.as_view(), name="assign-device"),
    path(
        "devices/<str:id>/localization/",
        DeviceLocalizationView.as_view(),
        name="device-localization",
    ),
    path(
        "users/<int:id>/localization/",
        UserLastLocalizationView.as_view(),
        name="user-localization",
    ),
]
