# AGENTS.md - SentimentNews

## Commands

```bash
# Django dev server
python manage.py runserver

# Celery worker (separate terminal) - optional
celery -A core worker -l info --pool=solo

# Celery Beat scheduler (separate terminal)
celery -A core beat -l info --schedule=celerybeat-schedule
```

## Required Setup

1. Copy `.env.example` to `.env`
2. Set `NEWS_API_KEY` (get from https://newsapi.org)
3. Run `python manage.py migrate`
4. Download NLTK data: `python -c "import nltk; nltk.download('vader_lexicon')"`

## Key Files

- `news/tasks.py` - Celery tasks: `fetch_and_save_articles`, `reanalyze_all_articles`
- `news/helpers.py` - `fetch_news()`, `analyze_sentiment()` using NLTK VADER
- `core/settings.py` - Django config, Celery Beat schedule (7200s = 2 hours)
- `news/models.py` - `NewsArticle` model

## Architecture

- Django 5.x with SQLite (dev) / PostgreSQL (prod via `DATABASE_URL`)
- Celery + Redis for async tasks
- NLTK VADER sentiment: compound ≥0.05 = Positive, ≤-0.05 = Negative, else Neutral
- NewsAPI for news data

## Env Variables

| Variable | Required | Default |
|----------|----------|---------|
| `NEWS_API_KEY` | Yes | - |
| `SECRET_KEY` | Yes | django-insecure-change-this-in-production |
| `DEBUG` | No | True |
| `DATABASE_URL` | No | - |
| `REDIS_URL` | No | redis://127.0.0.1:6379/1 |
| `NEWS_QUERY` | No | india |

## Notes

- No test suite exists (`news/tests.py` is empty)
- Celery Beat runs `fetch_and_save_articles` every 2 hours
- Sentiment analysis processes description truncated to 1000 chars