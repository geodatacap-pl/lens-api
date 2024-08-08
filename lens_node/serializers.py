from rest_framework import serializers
from .models import Endpoint, Detection
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = (
            'id', 'endpoint', 'device_id', 'resolution', 'detectionclass', 'timestamp', 'accuracy', 'position_x',
            'position_y', 'width', 'height', 'count')


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ('id', 'user', 'title', 'location')
