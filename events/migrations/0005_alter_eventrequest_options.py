# Generated by Django 5.0.1 on 2025-02-27 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_eventrequest_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventrequest',
            options={'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
    ]
