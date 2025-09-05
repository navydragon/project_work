# myapp/serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
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
    teams_count = serializers.SerializerMethodField()
    customer = CostomerSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Project
        fields = ('id','name','max_teams','teams_count','image','customer', 'tags','target', 'is_new','is_active')

    def get_teams_count(self, obj):
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
        filtered_projects = Project.objects.filter(category=obj.category, is_active=True)
        return ProjectShortSerializer(filtered_projects, many=True).data
