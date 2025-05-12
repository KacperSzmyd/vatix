from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import DeviceAssignSerializer
from .models import Device


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
