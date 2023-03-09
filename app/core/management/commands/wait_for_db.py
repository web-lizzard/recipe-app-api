"""Django command to wait for the database to be available"""

import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        try:
            self.check(databases=["default"])  # type: ignore
        except (OperationalError, Psycopg2Error):
            time.sleep(1)
            self.handle()
        else:
            self.stdout.write(self.style.SUCCESS("Database available!"))
