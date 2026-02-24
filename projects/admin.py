from django.contrib import admin
from django.urls import path, reverse
from .models import Semester, Team, Project, Participation, Tag, Customer, CPDSProject, Member, Setting
from .admin_export import export_teams_projects_excel, export_team_compositions_excel


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position')


@admin.register(Team)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'captain_fullname', 'captain_phone', 'captain_email', 'score')
    change_list_template = 'admin/projects/team/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'export-report-compositions/',
                self.admin_site.admin_view(export_team_compositions_excel),
                name='projects_team_export_compositions',
            ),
        ]
        return custom + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        changelist_url = reverse('admin:projects_team_changelist')
        extra_context['export_report_url'] = changelist_url.rstrip('/') + '/export-report-compositions/'
        extra_context['export_report_label'] = 'Экспорт составов команд'
        return super().changelist_view(request, extra_context)


@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'customer', 'description', 'link','is_new','is_active')


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'project', 'score')
    change_list_template = 'admin/projects/participation/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'export-report-teams-projects/',
                self.admin_site.admin_view(export_teams_projects_excel),
                name='projects_participation_export_teams_projects',
            ),
        ]
        return custom + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        changelist_url = reverse('admin:projects_participation_changelist')
        extra_context['export_report_url'] = changelist_url.rstrip('/') + '/export-report-teams-projects/'
        extra_context['export_report_label'] = 'Экспорт команд и проектов'
        return super().changelist_view(request, extra_context)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name','shortname','description','logo')


@admin.register(CPDSProject)
class CPDSProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'link', 'task', 'customer', 'course_title', 'team_size', 'required_by',
                    'functionality', 'required_skills', 'mentor_full_name', 'is_active')
    list_filter = ('status', 'customer', 'course_title', 'is_active')
    search_fields = ('name', 'problem', 'task', 'functionality', 'required_skills', 'mentor_full_name')
    readonly_fields = ('id',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'phone', 'team', 'score', 'group_name')  # Поля для отображения в списке
    search_fields = ('fullname', 'email', 'phone')  # Поля для поиска
    list_filter = ('team', 'group_name')  # Фильтры
    ordering = ('fullname',)  # Сортировка по имени


@admin.register(Setting)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'value')
