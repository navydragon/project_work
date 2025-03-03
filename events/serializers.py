from rest_framework import serializers
from .models import Event, EventRequest


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRequest
        fields = '__all__'