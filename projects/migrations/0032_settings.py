# Generated by Django 5.0.1 on 2025-02-21 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0031_team_old_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('value', models.CharField(max_length=300)),
            ],
        ),
    ]
