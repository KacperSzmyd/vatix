from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import DeviceAssignSerializer, LocalizationSerializer
from .models import Device, User, Localization


class AssigDeviceView(APIView):
    def post(self, request, id):
        try:
            device = Device.objects.get(device_id=id)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=404)

        serializer = DeviceAssignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(device=device)
            return Response({"status": "Device assigned"}, status=200)
        return Response(serializer.errors, status=400)


class DeviceLocalizationView(APIView):
    def post(self, request, id):
        try:
            device = Device.objects.get(device_id=id)
        except Device.DoesNotExist:
            return Response({"error": "Device not found."}, status=404)

        if device.user is None:
            return Response({"error": "Device is not assigned to ny user."}, status=400)

        serializer = LocalizationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(device=device)
            return Response({"status": "Localization recorded"}, status=201)

        return Response(serializer.errors, status=400)


class UserLastLocalizationView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        device = getattr(user, "device", None)
        
        if not device:
            return Response({"error": "User has no dedvice assigned"}, status=400)
        
        last_localization = device.localizations.order_by('-ping_time').first()
        
        if not last_localization:
            return Response({"error": "No localization data for this user"})
        
        data = {
            "latitude": last_localization.latitude,
            "longitude": last_localization.longitude,
            "ping_time": last_localization.ping_time
            
        }
        
        return Response(data, status=200)