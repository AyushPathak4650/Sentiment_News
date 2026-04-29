from django.core.management.base import BaseCommand
from news.tasks import fetch_and_save_articles


class Command(BaseCommand):
    help = 'Run migrations and fetch news'

    def handle(self, *args, **options):
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        self.stdout.write('Fetching news...')
        # Use .delay() for async Celery task or call synchronously if needed
        try:
            result = fetch_and_save_articles.delay()
            self.stdout.write(f'Task started with ID: {result.id}')
        except Exception as e:
            # Fallback: try calling synchronously
            self.stdout.write(f'Async failed, trying sync: {e}')
            try:
                fetch_and_save_articles()
            except Exception as e2:
                self.stdout.write(self.style.ERROR(f'Failed: {e2}'))
                return
        self.stdout.write(self.style.SUCCESS('Done!'))