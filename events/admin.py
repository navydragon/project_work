from django.contrib import admin
from django.urls import path, reverse

from .models import Event, EventRequest
from .admin_export import export_event_requests_excel


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("date", "discipline", "tutor", "group", "type", "classroom","direction")
    list_filter = ("date", "discipline", "tutor", "group", "type","direction")
    search_fields = ("discipline", "tutor", "group", "type", "classroom","direction")


@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ("event", "date", "full_name", "class_number", "school", "phone_number")
    list_filter = ("date", "event", "school")
    search_fields = ("full_name", "class_number", "school", "phone_number")

    change_list_template = "admin/events/eventrequest/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "export-report-eventrequests/",
                self.admin_site.admin_view(export_event_requests_excel),
                name="events_eventrequest_export_report",
            ),
        ]
        return custom + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        changelist_url = reverse("admin:events_eventrequest_changelist")
        extra_context["export_report_url"] = (
            changelist_url.rstrip("/") + "/export-report-eventrequests/"
        )
        extra_context["export_report_label"] = "Экспорт всех заявок (Excel)"
        return super().changelist_view(request, extra_context)