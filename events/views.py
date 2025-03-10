from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.mail import send_mail


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

        if created_requests:
            send_event_request_email(
                full_name=request.data.get("full_name"),
                school=request.data.get("school"),
                class_number=request.data.get("class_number"),
                phone_number=request.data.get("phone_number"),
                events=Event.objects.filter(id__in=events)
            )

        if errors:
            return Response({"created": created_requests, "errors": errors}, status=status.HTTP_207_MULTI_STATUS)

        return Response(created_requests, status=status.HTTP_201_CREATED)



def send_event_request_email(full_name, school, class_number, phone_number, events):
    subject = "Заявка на участие в мероприятиях"
    message = f"""
Вам поступила новая заявка на участие в мероприятиях Института экономики и финансов.

Имя - {full_name}
Школа - {school}
Класс - {class_number}
Номер телефона - {phone_number}

Выбранные мероприятия:
"""
    for idx, event in enumerate(events, 1):
        message += f"\n{idx}. {event.discipline} {event.date.strftime('%d.%m.%Y')}   {event.start_time}-{event.end_time} преп. {event.tutor} ауд. {event.classroom}"

    send_mail(
        subject,
        message,
        from_email=None,
        recipient_list=['priem-ief@yandex.ru'],
        fail_silently=False
    )
