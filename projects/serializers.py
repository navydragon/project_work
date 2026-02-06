# myapp/serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.core.cache import cache
from django.db.models import Count
import re
from .models import Team, Semester, Project, Participation, Customer, Tag, \
    Member, CPDSProject



class CPDSProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = CPDSProject
        fields = '__all__'

class CostomerSerializer (serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name')


class TeamShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id','name')


class ProjectShortSerializer(serializers.ModelSerializer):
    teams_count = serializers.IntegerField(read_only=True)
    customer = CostomerSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Project
        fields = ('id','name','max_teams','teams_count','image','customer', 'tags','target', 'is_new','is_active')

    def get_teams_count(self, obj):
        """
        Для обратной совместимости: если в queryset уже есть аннотация
        teams_count, используем её. Иначе считаем через obj.teams.count().
        """
        if hasattr(obj, "teams_count") and obj.teams_count is not None:
            return obj.teams_count
        return obj.teams.count()


class SemesterSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)
    class Meta:
        model = Semester
        fields = '__all__'


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'


class ParticipationShortSerializer(serializers.ModelSerializer):
    team = TeamShortSerializer(read_only=True)
    project = ProjectShortSerializer(read_only=True)
    class Meta:
        model = Participation

        fields = ('id','team','project','score')


class ProjectSerializer(serializers.ModelSerializer):
    participants = ParticipationShortSerializer(read_only=True, many=True)
    teams_count = serializers.SerializerMethodField()
    customer = CostomerSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'max_teams', 'teams_count', 'participants',
            'image', 'customer', 'task','problem', 'tags', 'description',
            'target','owner','context','is_active','is_new'
        )

    def get_teams_count(self, obj):
        return obj.teams.count()


class MemberSerializer (serializers.ModelSerializer):

    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        queryset = Member.objects.filter(team_id=team_id)

        return queryset
    class Meta:
        model = Member
        fields = '__all__'
        extra_kwargs = {
            'team': {'required': False},
        }




class TeamSerializer(serializers.ModelSerializer):
    participation = ParticipationShortSerializer(read_only=True, many=True)
    possible_projects = serializers.SerializerMethodField()
    members = MemberSerializer(read_only=True, many=True)
    semester = SemesterSerializer()
    
    class Meta:
        model = Team
        fields = '__all__'

    def validate_captain_email(self, value):
        """Валидация email капитана команды"""
        if value:
            email_validator = EmailValidator()
            email_validator(value)
        return value


    def validate_tutor_email(self, value):
        """Валидация email куратора"""
        if value:
            email_validator = EmailValidator()
            email_validator(value)
        return value

    def validate_name(self, value):
        """Валидация названия команды"""
        if not value or len(value.strip()) < 2:
            raise ValidationError("Название команды должно содержать минимум 2 символа")
        
        # Проверка на потенциально опасные символы
        if re.search(r'[<>"\']', value):
            raise ValidationError("Название команды содержит недопустимые символы")
        
        return value.strip()

    def validate_captain_fullname(self, value):
        """Валидация ФИО капитана"""
        if not value or len(value.strip()) < 2:
            raise ValidationError("ФИО капитана должно содержать минимум 2 символа")
        
        # Проверка на потенциально опасные символы
        if re.search(r'[<>"\']', value):
            raise ValidationError("ФИО капитана содержит недопустимые символы")
        
        return value.strip()

    def get_possible_projects(self, obj):
        category = obj.category
        if category is None:
            return []

        cache_key = f"possible_projects:{category}:active"
        cached_projects = cache.get(cache_key)

        if cached_projects is None:
            # Получаем все активные проекты нужной категории со связанными сущностями.
            # Считаем teams_count один раз через аннотацию, чтобы избежать N+1 при первичном построении кэша.
            queryset = (
                Project.objects.filter(category=category, is_active=True)
                .select_related("customer")
                .prefetch_related("tags", "teams")
                .annotate(teams_count=Count("teams"))
            )
            serialized = ProjectShortSerializer(queryset, many=True).data

            # В кэше храним данные без teams_count, чтобы это поле всегда было актуально.
            cached_projects = []
            for project in serialized:
                project_copy = dict(project)
                project_copy.pop("teams_count", None)
                cached_projects.append(project_copy)

            # TTL 5 минут: заметно снижает нагрузку, при этом
            # изменения проектов достаточно быстро попадут в кэш.
            cache.set(cache_key, cached_projects, timeout=300)

        # На этом этапе cached_projects не содержит teams_count.
        # Сам счетчик считаем отдельно агрегирующим запросом к Participation.
        project_ids = [p["id"] for p in cached_projects]
        if not project_ids:
            return []

        participation_counts = (
            Participation.objects.filter(project_id__in=project_ids)
            .values("project_id")
            .annotate(teams_count=Count("id"))
        )
        counts_map = {
            str(row["project_id"]): row["teams_count"] for row in participation_counts
        }

        result = []
        for project in cached_projects:
            project_with_count = dict(project)
            project_with_count["teams_count"] = counts_map.get(
                project["id"], 0
            )
            result.append(project_with_count)

        return result
