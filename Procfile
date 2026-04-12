web: gunicorn core.wsgi --bind 0.0.0.0:$PORT
worker: celery -A core worker --loglevel=info --concurrency=1
beat: celery -A core beat --loglevel=info --schedule=/app/celerybeat-schedule