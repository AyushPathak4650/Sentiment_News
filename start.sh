#!/bin/bash
set -e
pip install -r requirements.txt
python manage.py migrate --no-input
python manage.py shell << EOF
from news.tasks import fetch_and_save_articles
fetch_and_save_articles()
EOF
exec gunicorn core.wsgi --bind 0.0.0.0:$PORT