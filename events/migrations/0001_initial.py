# Generated by Django 5.0.1 on 2025-02-27 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(max_length=255, verbose_name='Направление подготовки')),
                ('profile', models.CharField(max_length=255, verbose_name='Профиль')),
                ('level', models.PositiveSmallIntegerField(verbose_name='Курс')),
                ('department', models.CharField(max_length=255, verbose_name='Читающая кафедра')),
                ('tutor', models.CharField(max_length=255, verbose_name='Преподаватель (спикер)')),
                ('discipline', models.CharField(max_length=255, verbose_name='Дисциплина')),
                ('weekday', models.CharField(max_length=50, verbose_name='День')),
                ('start_time', models.TimeField(verbose_name='Время начала')),
                ('end_time', models.TimeField(verbose_name='Время окончания')),
                ('classroom', models.CharField(max_length=50, verbose_name='Аудитория')),
                ('date', models.DateField(verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
            },
        ),
    ]
