"""
This command imports Nginx log file into Django DB.

Usage:
    python manage.py import_log <filename>


"""

from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = 'Import log file into DB.'

    def handle(self, *args, **options):
        import this