# News Aggregator with Sentiment Analysis

A production-grade full-stack web application that aggregates real-time news from global sources and performs automated sentiment analysis using Natural Language Processing.

## 🔧 Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Django 5.x, Python |
| **Task Queue** | Celery + Redis |
| **NLP** | NLTK VADER, TextBlob |
| **Database** | PostgreSQL (Production) / SQLite (Development) |
| **API** | NewsAPI |
| **Deployment** | Render, Gunicorn, WhiteNoise |

## 🚀 Key Features

- **Real-time News Aggregation** - Fetches articles from 50+ global sources via NewsAPI
- **Automated Sentiment Analysis** - Classifies articles as Positive/Negative/Neutral using VADER lexicon
- **Async Background Processing** - Celery Beat scheduler for continuous news fetching every 5 minutes
- **Interactive Dashboard** - Filter, search, and visualize sentiment trends
- **Redis Caching** - Performance optimization for database queries
- **Production-Ready** - Whitenoise static file serving, PostgreSQL support, error handling

## 📊 Architecture

```
[NewsAPI] → [Celery Worker] → [Sentiment Analysis (NLP)] → [PostgreSQL]
                                                          ↓
[User] ← [Django Views] ← [Redis Cache] ← [Dashboard UI]
```

## 💻 Local Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/SentimentNews.git
cd SentimentNews

# Virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your NEWS_API_KEY at https://newsapi.org

# Run
python manage.py migrate
python manage.py runserver
```

## 🌍 Live Demo

**https://sentiment-news-ajit.onrender.com**

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEWS_API_KEY` | API key from newsapi.org | Yes |
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Set to `False` for production | No |
| `DATABASE_URL` | PostgreSQL connection string | Production |

## ⭐ Highlights

- **Modular Architecture** - Clean separation between ingestion, processing, storage layers
- **Async Task Scheduling** - Celery Beat for periodic background jobs
- **Sentiment Classification** - Rule-based NLP using VADER (Valence Aware Dictionary)
- **Production Deployment** - Render-ready with PostgreSQL, Redis, Gunicorn

## 📄 License

MIT