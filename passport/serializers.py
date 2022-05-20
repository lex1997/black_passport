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


class TerroristSerializer(serializers.Serializer):
    lastname = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    middlename = serializers.CharField(max_length=255)
    birthday = serializers.DateField()
