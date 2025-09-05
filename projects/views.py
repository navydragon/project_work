# myapp/views.py
from rest_framework import viewsets, mixins, generics, status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.routers import APIRootView
# from django_ratelimit.decorators import ratelimit
# from django.utils.decorators import method_decorator

from .permissions import IsAdminOrReadOnly


from .models import Team, Semester, Project, Participation, Tag, Member, CPDSProject, Setting
from .serializers import TeamSerializer, SemesterSerializer, ProjectSerializer, \
    ParticipationSerializer, TagSerializer, MemberSerializer, CPDSProjectSerializer

from django.utils import timezone



# @method_decorator(ratelimit(key='ip', rate='100/h', method='GET'), name='list')
# @method_decorator(ratelimit(key='ip', rate='50/h', method='POST'), name='create')
# @method_decorator(ratelimit(key='ip', rate='200/h', method='PATCH'), name='partial_update')
# @method_decorator(ratelimit(key='ip', rate='200/h', method='PUT'), name='update')
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['semester']
    search_fields = ['name', 'captain_fullname']
    serializer_class = TeamSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Team.objects.prefetch_related('participation__project','participation__team','members').all()

    def get_permissions(self):
        """
        Разрешает обновление (PUT/PATCH) для всех пользователей,
        остальные операции требуют админских прав
        """
        if self.action in ['update', 'partial_update']:
            return [permissions.AllowAny()]
        return [IsAdminOrReadOnly()]

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Доступ к списку запрещен."}, status=status.HTTP_403_FORBIDDEN)


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Project.objects.prefetch_related('participants').all()


class ParticipationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer

    def get_permissions(self):
        """Динамически выбираем разрешения в зависимости от `open_registration`."""
        open_registration = Setting.objects.filter(code="open_registration").first()
        if not open_registration or open_registration.value != "true":
            return [IsAdminOrReadOnly()]  # Разрешение только для админов
        return [permissions.AllowAny()]


    def perform_create(self, serializer):
        team = get_object_or_404(Team, id=serializer.validated_data.get('team').id)
        project = get_object_or_404(Project, id=serializer.validated_data.get('project').id)

        if team.category != project.category:
            raise serializers.ValidationError({"message":"Балл команды меньше минимально допустимого"},400)

        if project.participants.count() >= project.max_teams:
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
    permission_classes = [IsAdminOrReadOnly]

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def perform_create(self, serializer):
        team_id = self.kwargs.get('team_id')
        serializer.save(team_id=team_id)


class ListCPDSProjects(generics.ListAPIView):
    queryset = CPDSProject.objects.filter(is_active=True)
    serializer_class = CPDSProjectSerializer
