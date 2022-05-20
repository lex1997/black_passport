from rest_framework import serializers

from .models import Passport

STATUS_CHOICES = (
    ('new', 'New'),
    ('active', 'Active'),
    ('off', 'Off'),
)

class PassportSerializer(serializers.Serializer):
    series = serializers.CharField(max_length=4)
    number = serializers.CharField(max_length=6)
    tms_create = serializers.DateTimeField(auto_now_add=True)


class TerroristSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    birthday = serializers.DateField()
    status = serializers.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    tms_create = serializers.DateTimeField(auto_now_add=True)
    tms_archive = serializers.DateTimeField(null=True, blank=True)