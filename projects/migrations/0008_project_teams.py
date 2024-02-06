# Generated by Django 5.0.1 on 2024-01-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_participation_project_alter_participation_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='teams',
            field=models.ManyToManyField(related_name='projects', through='projects.Participation', to='projects.team'),
        ),
    ]
