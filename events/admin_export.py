# Экспорт отчётов в Excel из Django Admin для заявок на мероприятия
import io

from django.http import HttpResponse
from openpyxl import Workbook

from .models import EventRequest


def _make_excel_response(rows, columns, filename):
    """Формирует HttpResponse с Excel-файлом."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Отчёт"
    ws.append(columns)

    for row in rows:
        ws.append([row.get(col, "") for col in columns])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def _format_time_range(e):
    start_time = str(e.start_time) if getattr(e, "start_time", None) else ""
    end_time = str(e.end_time) if getattr(e, "end_time", None) else ""
    return f"{start_time}-{end_time}" if (start_time or end_time) else ""


def _build_event_request_row(r):
    e = r.event
    return {
        "Дата заявки": r.date or "",
        "ФИО": r.full_name or "",
        "Класс": r.class_number or "",
        "Школа": r.school or "",
        "Телефон": r.phone_number or "",
        "Дата мероприятия": e.date or "",
        "Дисциплина": e.discipline or "",
        "Преподаватель": e.tutor or "",
        "Время": _format_time_range(e),
        "Аудитория": e.classroom or "",
        "Группа": e.group or "",
        "Тип занятия": e.type or "",
        "Направление": e.direction or "",
        "Профиль": e.profile or "",
        "Курс": e.level if e.level is not None else "",
        "Читающая кафедра": e.department or "",
    }


def export_event_requests_excel(_request):
    """Полный отчёт: все заявки на мероприятия (EventRequest)."""
    event_requests = (
        EventRequest.objects.select_related("event")
        .all()
        .order_by("event__date", "event__start_time", "date")
    )

    columns = [
        "Дата заявки",
        "ФИО",
        "Класс",
        "Школа",
        "Телефон",
        "Дата мероприятия",
        "Дисциплина",
        "Преподаватель",
        "Время",
        "Аудитория",
        "Группа",
        "Тип занятия",
        "Направление",
        "Профиль",
        "Курс",
        "Читающая кафедра",
    ]

    rows = [_build_event_request_row(r) for r in event_requests]

    return _make_excel_response(rows, columns, "report_event_requests.xlsx")

