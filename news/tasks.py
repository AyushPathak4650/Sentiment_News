import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def fetch_and_save_articles(self):
    """Fetch news from API and save to database with sentiment analysis."""
    try:
        from news.helpers import fetch_news, analyze_sentiment
        from news.models import NewsArticle
        from django.utils.dateparse import parse_datetime
        from django.conf import settings
        
        query = getattr(settings, 'NEWS_QUERY', 'india')
        days = 1
        
        articles = fetch_news(query, days=days)
        
        if not articles:
            logger.info("No articles found from API")
            return {'status': 'no_articles', 'processed': 0, 'saved': 0}
        
        processed = 0
        saved_count = 0
        
        for article in articles:
            try:
                url = article.get('url')
                if not url:
                    continue
                
                title = (article.get('title') or '')[:255]
                description = (article.get('description') or '')[:2000]
                source_name = (article.get('source', {}).get('name') or '')[:100]
                published_at_str = article.get('publishedAt', '')
                image_url = article.get('urlToImage', '') or ''
                
                published_at = parse_datetime(published_at_str)
                if published_at is None:
                    published_at = timezone.now()
                elif timezone.is_naive(published_at):
                    published_at = timezone.make_aware(published_at)
                
                sentiment = analyze_sentiment(description[:1000]) if description else 'Neutral'
                
                defaults = {
                    'title': title,
                    'description': description,
                    'source_name': source_name,
                    'published_at': published_at,
                    'image_url': image_url,
                    'sentiment': sentiment,
                }
                
                obj, created = NewsArticle.objects.get_or_create(url=url, defaults=defaults)
                processed += 1
                if created:
                    saved_count += 1
                    
            except Exception as e:
                logger.warning(f"Failed to process article: {e}")
                continue
        
        logger.info(f"Fetched {processed} articles, saved {saved_count} new")
        return {'status': 'success', 'processed': processed, 'saved': saved_count}
        
    except Exception as e:
        logger.error(f"Task failed: {e}")
        raise self.retry(exc=e, countdown=60)


@shared_task
def reanalyze_all_articles():
    """Re-analyze all existing articles for sentiment."""
    from news.helpers import analyze_sentiment
    from news.models import NewsArticle
    
    articles = NewsArticle.objects.all()
    count = 0
    for article in articles:
        if article.description:
            new_sentiment = analyze_sentiment(article.description[:1000])
            article.sentiment = new_sentiment
            article.save()
            count += 1
    return f'Re-analyzed {count} articles'