from django.db import models
import uuid


class Semester(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    position = models.IntegerField()
    choose_teams = models.BooleanField(default=False)
    choose_projects = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    captain_fullname = models.CharField(max_length=255)
    captain_phone = models.CharField(max_length=20, blank=True, null=True)
    captain_email = models.EmailField(blank=True, null=True)
    tutor_fullname = models.CharField(max_length=20, blank=True, null=True)
    tutor_email = models.EmailField(blank=True, null=True)
    group_name = models.CharField(max_length=20, blank=True, null=True)
    score = models.PositiveIntegerField(blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='teams')
    category = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Member (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    score = models.IntegerField(null=True, blank=True)


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects')
    owner = models.CharField(max_length=255, blank=True, null=True)
    target = models.TextField(blank=True, null=True)
    problem = models.TextField(blank=True, null=True)
    task = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    min_score = models.PositiveIntegerField(blank=True, null=True)
    max_score = models.PositiveIntegerField(blank=True, null=True)
    max_teams = models.PositiveIntegerField(blank=True, null=True)
    image = models.FileField(upload_to='projects',null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='projects')
    teams = models.ManyToManyField(Team, through='Participation', related_name='projects')
    category = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='projects')

    def __str__(self):
        return self.name


class Participation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='participation')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='participants')
    choose_date = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.team.name} - {self.project.name}"




