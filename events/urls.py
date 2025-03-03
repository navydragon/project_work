from django.urls import path, include

from events.views import EventListAPIView, EventDetailAPIView, EventRequestAPIView

urlpatterns = [
    path('events/', EventListAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),
    path('requests/', EventRequestAPIView.as_view(), name='event-detail'),
]