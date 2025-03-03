from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event
from events.serializers import EventSerializer, EventRequestSerializer


class EventListAPIView(APIView):
    def get(self, request):
        events = Event.objects.all().order_by('date')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventDetailAPIView(APIView):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


class EventRequestAPIView(APIView):
    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        requests = event.requests.order_by('date')
        serializer = EventRequestSerializer(requests, many=True)
        return Response(serializer.data)


    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        data = request.data.copy()
        data["event"] = event.id
        serializer = EventRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)