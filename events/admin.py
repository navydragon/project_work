from django.contrib import admin
from .models import Event, EventRequest


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("date", "discipline", "tutor", "group", "type", "classroom")
    list_filter = ("date", "discipline", "tutor", "group", "type")
    search_fields = ("discipline", "tutor", "group", "type", "classroom")


@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ("event", "date", "full_name", "class_number", "school", "phone_number")
    list_filter = ("date", "event", "school","direction")
    search_fields = ("full_name", "class_number", "school", "phone_number","direction")