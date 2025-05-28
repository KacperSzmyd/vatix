from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .serializers import DeviceAssignSerializer, LocationSerializer, DeviceSerializer
from .models import Device, User, Location
from datetime import timedelta, datetime
import csv


class AssigDeviceView(APIView):
    def post(self, request, id):
        try:
            device = Device.objects.get(device_id=id)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=404)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "No user id provided"}, status=400)

        user = get_object_or_404(User, id=user_id)

        serializer = DeviceAssignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(device=device)
            return Response({"status": "Device assigned"}, status=200)
        return Response(serializer.errors, status=400)


class DeviceLocationView(APIView):
    def post(self, request, id):
        try:
            device = Device.objects.get(device_id=id)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=404)

        if device.user is None:
            return Response({"error": "Device is not assigned to ny user."}, status=400)

        serializer = LocationSerializer(data=request.data)

        if serializer.is_valid():
            new_ping_time = serializer.validated_data["ping_time"]
            last_location = device.location.order_by("-ping_time").first()

            if last_location and (new_ping_time - last_location.ping_time) < timedelta(
                minutes=5
            ):
                return Response(
                    {
                        "error": "Location update too soon. Please wait before sending another ping"
                    }
                )

            serializer.save(device=device)
            return Response({"status": "Location recorded"}, status=201)

        return Response(serializer.errors, status=400)


class UserLastLocationView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        device = getattr(user, "device", None)

        if not device:
            return Response({"error": "User has no device assigned"}, status=400)

        last_location = device.location.order_by("-ping_time").first()

        if not last_location:
            return Response({"error": "No location data for this user"})

        data = {
            "latitude": last_location.latitude,
            "longitude": last_location.longitude,
            "ping_time": last_location.ping_time,
        }

        return Response(data, status=200)


class UserLoctionView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=400)

        date = request.query_params.get("date")
        if not date:
            return Response({"error": "no date provided"}, status=400)

        device = getattr(user, "device", None)
        locations = device.locations.filter(ping_time__date=date).order_by("ping_time")

        if not locations:
            return Response([], status=200)

        results = LocationSerializer(locations, many=True)
        return Response(results.data)


class MapView(APIView):
    def get(self, request):
        result = []

        devices = Device.objects.exclude(user=None)

        for device in devices:
            last_location = device.location.order_by("-ping_time").first()
            if not last_location:
                continue

            result.append(
                {
                    "user": {
                        "id": device.user.id,
                        "name": f"{device.user.first_name} {device.user.last_name}",
                    },
                    "device_id": device.device_id,
                    "latitude": last_location.latitude,
                    "longitude": last_location.longitude,
                    "timestamp": last_location.ping_time,
                }
            )

        return Response(result)


class UnassignDeviceView(APIView):
    def post(self, request, id):
        try:
            device = Device.objects.get(device_id=id)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."})

        if device.user is None:
            return Response({"status": "Device is already unassigned"}, status=200)

        device.user = None
        device.save()
        return Response({"status": "Device unassigned"}, status=200)


class DeviceListView(APIView):
    def get(self, request):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)


class DeviceLocationHistoryView(APIView):
    def get(self, request, id):
        device = get_object_or_404(Device, device_id=id)

        days = int(request.query_params.get("days"))
        if not days:
            days = 1

        requested_day = datetime.today() - timedelta(days=days)

        locations = device.locations.filter(ping_time__date__gte=requested_day)

        if not locations:
            return Response([], status=200)

        results = LocationSerializer(locations, many=True)
        return Response(results.data, status=200)


class ExportLocationsToCsvView(APIView):
    def get(self, request, id):
        try:
            device = Device.objects.get(device_id=id)
        except Device.DoesNotExist:
            return Response({"error": "No device with that id"}, status=400)

        locations = device.locations.all().order_by("ping_time")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="device_{}_locations.csv"'.format(id)
        )

        if not locations:
            return Response([], status=200)
        writer = csv.writer(response)
        writer.writerow(["latitude", "longitude", "ping_time"])

        for location in locations:
            writer.writerow([location.latitude, location.longitude, location.ping_time])

        return response
