from django.db import models
from django.contrib.auth.models import User


class Endpoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=32)
    location = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Detection(models.Model):
    endpoint = models.ForeignKey(Endpoint, on_delete=models.SET_NULL, null=True)
    device_id = models.CharField(max_length=32)
    resolution = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now=True)
    detectionclass = models.CharField(max_length=32)
    accuracy = models.DecimalField(max_digits=10, decimal_places=4)
    position_x = models.DecimalField(max_digits=10, decimal_places=4)
    position_y = models.DecimalField(max_digits=10, decimal_places=4)
    width = models.DecimalField(max_digits=10, decimal_places=4)
    height = models.DecimalField(max_digits=10, decimal_places=4)
    count = models.IntegerField()
