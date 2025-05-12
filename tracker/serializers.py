from rest_framework import serializers
from .models import User, Device, Location


class DeviceSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ["device_id", "user_id", "user_name"]

    def get_user_id(self, obj):
        return obj.user.id if obj.user else None

    def get_user_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return None


class DeviceAssignSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not Found.")
        return value

    def save(self, device):
        user_id = self.validated_data["user_id"]
        new_user = User.objects.get(id=user_id)

        if hasattr(new_user, "device"):
            old_device = new_user.device
            old_device.user = None
            old_device.save()

        device.user = new_user
        device.save()
        return device


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["latitude", "longitude", "ping_time"]
