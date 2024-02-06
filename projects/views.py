# myapp/views.py
from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework import serializers


from .models import Team, Semester, Project, Participation, Tag, Member
from .serializers import TeamSerializer, SemesterSerializer, ProjectSerializer, \
    ParticipationSerializer, TagSerializer, MemberSerializer

from django.utils import timezone

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['semester']
    search_fields = ['name', 'captain_fullname']
    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.prefetch_related('participation__project','participation__team','members').all()


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def perform_create(self, serializer):
        last_position = Semester.objects.all().order_by('-position').first()
        if last_position:
            serializer.validated_data['position'] = last_position.position + 1
        else:
            serializer.validated_data['position'] = 1

        serializer.save()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.prefetch_related('participants').all()


class ParticipationViewSet (viewsets.ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer

    def perform_create(self, serializer):
        team = get_object_or_404(Team, id=serializer.validated_data.get('team').id)
        project = get_object_or_404(Project, id=serializer.validated_data.get('project').id)

        if team.category != project.category:
            raise serializers.ValidationError({"message":"Балл команды меньше минимально допустимого"},400)


        if project.participants.count() > project.max_teams:
            raise serializers.ValidationError({"message":"Достигнуто максимальное количество участников проекта."},400)

        serializer.validated_data['choose_date'] = timezone.now()

        existing_participation = Participation.objects.filter(team=team).first()

        if existing_participation:
            for key, value in serializer.validated_data.items():
                setattr(existing_participation, key, value)
            # Сохраняем обновленный экземпляр
            existing_participation.save()
        else:
            # Если экземпляр не существует, создаем новый
            serializer.save()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def perform_create(self, serializer):
        team_id = self.kwargs.get('team_id')
        serializer.save(team_id=team_id)