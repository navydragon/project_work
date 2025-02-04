# yourapp/management/commands/import_teams.py
import pandas as pd
from django.core.management.base import BaseCommand
from projects.models import Team, Semester

class Command(BaseCommand):
    help = 'Import teams from Excel file'

    def handle(self, *args, **kwargs):
        file_path = 'files/teams2.xlsx'
        df = pd.read_excel(file_path)
        # Assuming you have a semester instance, replace with appropriate logic
        semester = Semester.objects.last()  # Adjust this as per your requirements
        print("Columns in the Excel file:", df.columns)
        for _, row in df.iterrows():
            Team.objects.create(
                name=row['name'],
                captain_fullname=row['captain_fullname'],
                tutor_fullname=row['tutor_fullname'],
                tutor_email=row['tutor_email'],
                group_name=row['group_name'],
                category=row['category'],
                previous_project_name=row['previous_project_name'],
                semester=semester
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
