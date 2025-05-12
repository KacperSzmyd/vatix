from django.urls import path
from .views import AssigDeviceView

urlpatterns = [
    path("devices/<str:id>/assign", AssigDeviceView.as_view(), name="assign-device")
]
