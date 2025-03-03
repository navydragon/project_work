# yourapp/management/commands/import_teams.py
import pandas as pd
from django.core.management.base import BaseCommand
from events.models import Event

class Command(BaseCommand):
    help = 'Import events from Excel file'

    def handle(self, *args, **kwargs):
        file_path = 'files/events.xlsx'
        df = pd.read_excel(file_path)
        # Assuming you have a semester instance, replace with appropriate logic
        event = Event.objects.last()  # Adjust this as per your requirements
        print("Columns in the Excel file:", df.columns)
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
