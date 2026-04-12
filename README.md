# News Insight

A production-ready Django news aggregator with sentiment analysis and automatic news fetching.

## Features

- Real-time news fetching from NewsAPI
- Sentiment analysis (Positive/Negative/Neutral) using NLTK VADER
- Automatic periodic fetching with Celery Beat
- Clean dashboard with Chart.js visualization
- Redis caching support
- Error handling and custom error pages
- Production-ready settings

## Tech Stack

- Django 5.x
- Celery + Redis
- NLTK for sentiment analysis
- Bootstrap 5 for UI

## Quick Start (Local)

```bash
# Clone and navigate
cd SentimentNews

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your NEWS_API_KEY
# Get free API key at https://newsapi.org

# Run migrations
python manage.py migrate

# Run the server
python manage.py runserver
```

Visit http://127.0.0.1:8000

## Running Background Tasks (Local)

```bash
# Terminal 1 - Django server
python manage.py runserver

# Terminal 2 - Celery worker (Windows requires --pool=solo)
celery -A core worker -l info --pool=solo

# Terminal 3 - Celery Beat scheduler
celery -A core beat -l info
```

## Deploy to Render

### 1. Push to GitHub
Commit all files and push to a GitHub repository.

### 2. Create Render Account
Sign up at https://render.com

### 3. Create Web Service
- Dashboard → New → Web Service
- Connect your GitHub repo
- Set root directory (if needed)
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn core.wsgi --bind 0.0.0.0:$PORT`

### 4. Add Environment Variables
In Render dashboard, add these env vars:
```
NEWS_API_KEY=your_newsapi_key
SECRET_KEY=generate_a_strong_key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
```

### 5. Add Redis (Background Worker)
- Dashboard → New → Redis
- Note the Redis connection URL

### 6. Add Celery Worker (Optional)
- Dashboard → New → Background Worker
- Command: `celery -A core worker -l info`
- Add Redis URL to env vars

## Manual Task Trigger

```bash
python manage.py shell -c "from news.tasks import fetch_and_save_articles; fetch_and_save_articles()"
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `NEWS_API_KEY` | NewsAPI.org key | Required |
| `SECRET_KEY` | Django secret | Auto-generated |
| `DEBUG` | Debug mode | True |
| `ALLOWED_HOSTS` | Allowed hosts | localhost,127.0.0.1 |
| `CELERY_BROKER_URL` | Redis URL | redis://localhost:6379 |
| `NEWS_QUERY` | Search query | india |
| `REDIS_URL` | Redis cache | redis://127.0.0.1:6379/1 |

## License

MIT