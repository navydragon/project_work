# yourapp/management/commands/import_teams.py
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from events.models import Event

class Command(BaseCommand):
    help = 'Import events from Excel file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear events table before import',
        )

    def handle(self, *args, **kwargs):
        file_path = 'files/events.xlsx'
        df = pd.read_excel(file_path)
        print("Columns in the Excel file:", df.columns)

        with transaction.atomic():
            if kwargs.get('clear'):
                Event.objects.all().delete()

            for _, row in df.iterrows():
                if row['has'] == 'да':
                    Event.objects.create(
                        direction=row['direction'],
                        profile=row['profile'],
                        level=row['level'],
                        department=row['department'],
                        tutor=row['tutor'],
                        discipline=row['discipline'],
                        weekday=row['weekday'],
                        start_time=row['start_time'],
                        end_time=row['end_time'],
                        classroom=row['classroom'],
                        date=row['date'],
                        group=row['group'],
                        type=row['type'],
                    )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
