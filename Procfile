web: gunicorn core.wsgi --chdir .
worker: celery -A core worker -l info --pool=solo
beat: celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler