from django.db import models


class Event(models.Model):
    direction = models.CharField(max_length=255, verbose_name="Направление подготовки", blank=True, null=True)
    profile = models.CharField(max_length=255, verbose_name="Профиль", blank=True, null=True)
    level = models.PositiveSmallIntegerField(verbose_name="Курс", blank=True, null=True)
    department = models.CharField(max_length=255, verbose_name="Читающая кафедра", blank=True, null=True)
    tutor = models.CharField(max_length=255, verbose_name="Преподаватель (спикер)", blank=True, null=True)
    discipline = models.CharField(max_length=255, verbose_name="Дисциплина", blank=True, null=True)
    weekday = models.CharField(max_length=50, verbose_name="День", blank=True, null=True)
    start_time = models.TimeField(verbose_name="Время начала", blank=True, null=True)
    end_time = models.TimeField(verbose_name="Время окончания", blank=True, null=True)
    classroom = models.CharField(max_length=50, verbose_name="Аудитория", blank=True, null=True)
    date = models.DateField(verbose_name="Дата", blank=True, null=True)
    group = models.CharField(max_length=255, verbose_name="Группа", blank=True, null=True)
    type = models.CharField(max_length=255, verbose_name="Тип занятия", blank=True, null=True)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return f"{self.date} - {self.discipline} ({self.tutor})"


class EventRequest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="requests", verbose_name="Мероприятие")
    date = models.DateField(verbose_name="Дата заявки", auto_now_add=True)
    full_name = models.CharField(max_length=500, verbose_name="ФИО")
    class_number = models.CharField(max_length=30, verbose_name="Класс")
    school = models.CharField(max_length=999, verbose_name="Школа")
    phone_number = models.CharField(max_length=50, verbose_name="Телефон")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"