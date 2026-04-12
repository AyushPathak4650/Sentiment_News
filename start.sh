#!/bin/bash
set -e
python manage.py migrate --no-input
python manage.py collectstatic --no-input
celery -A core worker --loglevel=info --concurrency=1 &
celery -A core beat --loglevel=info --schedule=/app/celerybeat-schedule &
exec gunicorn core.wsgi --bind 0.0.0.0:$PORT