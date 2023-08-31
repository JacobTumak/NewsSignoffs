# yourapp/management/commands/populate_demo_data.py
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate demo data for the Editor app"

    def handle(self, *args, **options):
        self.create_assignments()

        self.stdout.write(self.style.SUCCESS("Demo Assignments data populated successfully"))

    def create_assignments(self):
        pass
