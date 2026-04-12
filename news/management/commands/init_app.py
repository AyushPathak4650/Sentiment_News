from django.core.management.base import BaseCommand
from news.tasks import fetch_and_save_articles


class Command(BaseCommand):
    help = 'Run migrations and fetch news'

    def handle(self, *args, **options):
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        self.stdout.write('Fetching news...')
        fetch_and_save_articles()
        self.stdout.write(self.style.SUCCESS('Done!'))