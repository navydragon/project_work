# Экспорт отчётов в Excel из Django Admin
import io
from django.http import HttpResponse
from openpyxl import Workbook

from .models import Participation, Team


def _make_excel_response(rows, columns, filename):
    """Формирует HttpResponse с Excel-файлом."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Отчёт"
    ws.append(columns)
    for row in rows:
        ws.append([row.get(col, '') for col in columns])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def export_teams_projects_excel(request):
    """Отчёт 1: Капитан команды, Название команды, Группа, Наставник, Название проекта, Заказчик."""
    participations = Participation.objects.select_related(
        'team', 'project', 'project__customer'
    ).all()

    columns = ['Капитан команды', 'Название команды', 'Группа', 'Наставник', 'Название проекта', 'Заказчик']
    rows = []
    for p in participations:
        rows.append({
            'Капитан команды': p.team.captain_fullname or '',
            'Название команды': p.team.name or '',
            'Группа': p.team.group_name or '',
            'Наставник': p.team.tutor_fullname or '',
            'Название проекта': p.project.name if p.project else '',
            'Заказчик': p.project.customer.name if p.project and p.project.customer else '',
        })

    return _make_excel_response(rows, columns, 'report_teams_projects.xlsx')


def export_team_compositions_excel(request):
    """Отчёт 2: Составы команд — одна строка на участника (капитан первым)."""
    teams = Team.objects.prefetch_related('members').all()

    columns = ['Название команды', 'ФИО', 'Email', 'Телефон', 'Группа', 'Роль']
    rows = []
    for team in teams:
        rows.append({
            'Название команды': team.name or '',
            'ФИО': team.captain_fullname or '',
            'Email': team.captain_email or '',
            'Телефон': team.captain_phone or '',
            'Группа': team.group_name or '',
            'Роль': 'Капитан',
        })
        for member in team.members.all():
            rows.append({
                'Название команды': team.name or '',
                'ФИО': member.fullname or '',
                'Email': member.email or '',
                'Телефон': member.phone or '',
                'Группа': member.group_name or team.group_name or '',
                'Роль': 'Участник',
            })

    return _make_excel_response(rows, columns, 'report_team_compositions.xlsx')
