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

    def post(self, request):
        events = request.data.get("events", [])
        errors = []
        created_requests = []

        for event_id in events:
            event = Event.objects.filter(id=event_id).first()
            if not event:
                errors.append({"event_id": event_id, "error": "Мероприятие не найдено"})
                continue

            data = request.data.copy()
            data["event"] = event.id
            serializer = EventRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                created_requests.append(serializer.data)
            else:
                errors.append({"event_id": event_id, "errors": serializer.errors})

        if errors:
            return Response({"created": created_requests, "errors": errors}, status=status.HTTP_207_MULTI_STATUS)

        return Response(created_requests, status=status.HTTP_201_CREATED)