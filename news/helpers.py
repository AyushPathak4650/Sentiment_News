import nltk
from decouple import config
import requests
import datetime
import logging

logger = logging.getLogger(__name__)

try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
except Exception as e:
    logger.warning(f"Failed to load VADER: {e}")
    sia = None

try:
    from textblob import TextBlob
    tb_available = True
except ImportError:
    logger.warning("TextBlob not installed, falling back to VADER only")
    tb_available = False

POSITIVE_KEYWORDS = {
    'surge', 'soar', 'rally', 'gain', 'rise', 'growth', 'boost', 'increase', 'up',
    'breakthrough', 'success', 'win', 'achievement', 'record', 'high', 'peak',
    'improve', 'recover', 'rebound', 'positive', 'bullish', 'optimistic', 'strong',
    'profit', 'beat', 'exceed', 'outperform', 'upgrade', 'buy', 'recommend',
    'milestone', 'deal', 'agreement', 'partnership', 'launch', 'expand', 'invest',
    'historic', 'landmark', 'revolutionary', 'innovative', 'lead', 'winner', 'best'
}

NEGATIVE_KEYWORDS = {
    'crash', 'plunge', 'drop', 'fall', 'decline', 'down', 'loss', 'lose',
    'crisis', 'scandal', 'fraud', 'investigation', 'lawsuit', 'bankruptcy',
    'layoff', 'cut', 'reduce', 'negative', 'bearish', 'pessimistic', 'weak',
    'miss', 'underperform', 'downgrade', 'sell', 'warning', 'risk', 'threat',
    'fire', 'resign', 'corruption', 'hack', 'breach', 'fail',
    'delay', 'cancel', 'suspend', 'halt', 'shock', 'disaster', 'tragedy',
    'death', 'kill', 'injury', 'accident', 'conflict', 'war', 'sanction'
}

CONTEXT_MODIFIERS = {
    'not': -1,
    "n't": -1,
    'no': -1,
    'never': -1,
    'without': -1,
    'despite': -0.5,
    'although': 0,
    'but': 0,
    'however': 0,
}


def analyze_sentiment(text):
    """Enhanced sentiment analysis combining VADER, TextBlob, and keyword boosting."""
    if not text:
        return "Neutral"
    
    text_lower = text.lower()[:1500]
    
    vader_score = 0
    if sia:
        try:
            vader_scores = sia.polarity_scores(text_lower)
            vader_score = vader_scores['compound']
        except Exception as e:
            logger.debug(f"VADER error: {e}")
    
    tb_score = 0
    if tb_available:
        try:
            blob = TextBlob(text_lower)
            tb_score = blob.sentiment.polarity
        except Exception as e:
            logger.debug(f"TextBlob error: {e}")
    
    keyword_boost = 0
    words = set(text_lower.split())
    
    pos_count = len(words & POSITIVE_KEYWORDS)
    neg_count = len(words & NEGATIVE_KEYWORDS)
    
    if pos_count + neg_count > 0:
        keyword_boost = (pos_count - neg_count) / (pos_count + neg_count + 1)
        keyword_boost *= 0.3
    
    has_negation = any(mod in text_lower for mod in CONTEXT_MODIFIERS)
    
    if tb_available:
        combined_score = (vader_score * 0.4) + (tb_score * 0.3) + (keyword_boost * 0.3)
    else:
        combined_score = (vader_score * 0.6) + (keyword_boost * 0.4)
    
    if has_negation and abs(combined_score) > 0.1:
        combined_score *= 0.5
    
    if combined_score >= 0.03:
        return "Positive"
    elif combined_score <= -0.03:
        return "Negative"
    return "Neutral"


def fetch_news(query, days=3):
    today = datetime.date.today()
    from_date = today - datetime.timedelta(days=days)
    
    NEWS_API_KEY = config('NEWS_API_KEY', default='')
    if not NEWS_API_KEY:
        logger.warning("NEWS_API_KEY not configured")
        return []
    
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
    NEWS_API_KEY = config('NEWS_API_KEY', default='')
    if not NEWS_API_KEY:
        return []
    
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