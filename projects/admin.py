from django.contrib import admin

from django.contrib import admin
from .models import Semester, Team, Project, Participation, Tag, Customer, CPDSProject, Member


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position')


@admin.register(Team)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'captain_fullname', 'captain_phone', 'captain_email', 'score')


@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'customer', 'description', 'link')


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'project', 'score')


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