from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"


class Device(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="device"
    )

    def __str__(self):
        return str(self.device_id)


class Location(models.Model):
    # Optional on_delete=models.CASCADE in case when historical location data is irrelevant
    device = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        related_name="location",
        blank=True,
        null=True,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    ping_time = models.DateTimeField()

    def __str__(self):
        return f"{self.device.device_id} @ {self.ping_time}"
