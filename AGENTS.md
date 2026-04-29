# AGENTS.md - SentimentNews

## Project
Django 5.x news aggregator with Celery background tasks and NLTK VADER sentiment analysis. Deployed on Render.

## Setup
```bash
# 1. Create venv and install
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# 2. Copy env and add API key
cp .env.example .env
# Edit .env: add NEWS_API_KEY from https://newsapi.org
```

## Run Commands
```bash
# Dev server (terminal 1)
python manage.py runserver

# Celery worker (terminal 2) - fetches news every 2 hours
celery -A core worker -l info --pool=solo

# Celery beat scheduler (terminal 3) - optional, for periodic tasks
celery -A core beat -l info --schedule=/app/celerybeat-schedule
```

## Test Execution
```bash
# Run tests
python manage.py test news

# Test news fetching task directly
python manage.py shell -c "from news.tasks import fetch_and_save_articles; print(fetch_and_save_articles())"
```

## Key Architecture
- **URL routing**: `core/urls.py` → `news/urls.py`
- **Sentiment logic**: `news/helpers.py` - VADER compound score thresholds
- **Scheduled task**: `core/settings.py:148-153` - runs every 7200s (2 hours)
- **Models**: `news/models.py:NewsArticle` - indexed on `published_at`, `sentiment`, `created_at`
- **Sentiment thresholds** (from `news/helpers.py:102-106`): compound ≥ 0.03 → Positive, ≤ -0.03 → Negative, else Neutral

## Environment Variables
| Variable | Required | Notes |
|----------|----------|-------|
| `NEWS_API_KEY` | Yes | Get from newsapi.org |
| `SECRET_KEY` | Yes | Django secret |
| `DEBUG` | No | Default True |
| `CELERY_BROKER_URL` | No | Redis URL for production |

## Production (Render)
- Uses SQLite by default; `DATABASE_URL` swaps to PostgreSQL
- `Procfile` defines: web, worker, beat processes
- `start.sh` runs migrations + collectstatic + starts all processes