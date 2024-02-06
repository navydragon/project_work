from django.contrib import admin

from django.contrib import admin
from .models import Semester, Team, Project, Participation, Tag, Customer

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