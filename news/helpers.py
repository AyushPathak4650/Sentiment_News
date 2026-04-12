from decouple import config
import requests
import datetime
import logging

logger = logging.getLogger(__name__)

try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
except:
    sia = None

def analyze_sentiment(text):
    if not text:
        return "Neutral"
    
    if sia is None:
        return "Neutral"
    
    try:
        scores = sia.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            return "Positive"
        elif compound <= -0.05:
            return "Negative"
        return "Neutral"
    except Exception as e:
        logger.warning(f"Sentiment analysis failed: {e}")
        return "Neutral"


def fetch_news(query, days=3):
    today = datetime.date.today()
    from_date = today - datetime.timedelta(days=days)
    
    NEWS_API_KEY = config('NEWS_API_KEY')
    BASE_URL = 'https://newsapi.org/v2/'
    
    url = f"{BASE_URL}everything?q={query}&from={from_date}&to={today}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    logger.info(f"Fetching news from: {url[:50]}...")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get('articles', [])
        else:
            logger.error(f"API returned status {response.status_code}: {response.text[:200]}")
            return []
    except Exception as e:
        logger.error(f"Failed to fetch news: {e}")
        return []


def fetch_by_category(category='general'):
    NEWS_API_KEY = config('NEWS_API_KEY')
    BASE_URL = 'https://newsapi.org/v2/'
    
    url = f"{BASE_URL}everything?q={category}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get('articles', [])
        return []
    except Exception as e:
        logger.error(f"Failed to fetch by category: {e}")
        return []