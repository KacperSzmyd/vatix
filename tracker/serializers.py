from rest_framework import serializers
from .models import User, Device, Localization


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


class LocalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localization
        fields = ["latitude", "longitude", "ping_time"]

