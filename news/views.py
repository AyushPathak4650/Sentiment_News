from django.shortcuts import render
from django.http import JsonResponse
from .models import NewsArticle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Case, When
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


def dashboard(request):
    """Dashboard with sentiment stats and filtered articles."""
    search_term = request.GET.get('q', '')
    sentiment_filter = request.GET.get('sentiment', '')
    source_filter = request.GET.get('source', '')
    
    articles_qs = NewsArticle.objects.all().order_by('-published_at')
    
    if search_term:
        articles_qs = articles_qs.filter(
            Q(title__icontains=search_term) | 
            Q(description__icontains=search_term) |
            Q(source_name__icontains=search_term)
        )
    
    if sentiment_filter:
        articles_qs = articles_qs.filter(sentiment=sentiment_filter)
    
    if source_filter:
        articles_qs = articles_qs.filter(source_name=source_filter)
    
    articles_qs = articles_qs.select_related()
    
    stats = NewsArticle.objects.aggregate(
        positive=Count(Case(When(sentiment='Positive', then=1))),
        negative=Count(Case(When(sentiment='Negative', then=1))),
        neutral=Count(Case(When(sentiment='Neutral', then=1)))
    )
    
    sources = list(NewsArticle.objects.values_list('source_name', flat=True).distinct().order_by('source_name'))
    
    paginator = Paginator(articles_qs, 9)
    page = request.GET.get('page', 1)
    
    try:
        articles = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        articles = paginator.page(1)
    
    last_updated = NewsArticle.objects.order_by('-updated_at').values('updated_at').first()
    latest_articles = list(NewsArticle.objects.order_by('-published_at')[:5])
    
    context = {
        'articles': articles,
        'stats': stats,
        'search_term': search_term,
        'sentiment_filter': sentiment_filter,
        'source_filter': source_filter,
        'sources': sources,
        'total_articles': NewsArticle.objects.count(),
        'last_updated': last_updated['updated_at'] if last_updated else None,
        'latest_articles': latest_articles,
    }
    return render(request, 'news/dashboard.html', context)


def home(request):
    """Browse all articles with pagination."""
    search_term = request.GET.get('q', '')
    sentiment_filter = request.GET.get('sentiment', '')
    source_filter = request.GET.get('source', '')
    
    articles_qs = NewsArticle.objects.all().order_by('-published_at')
    
    if search_term:
        articles_qs = articles_qs.filter(
            Q(title__icontains=search_term) | 
            Q(description__icontains=search_term) |
            Q(source_name__icontains=search_term)
        )
    
    if sentiment_filter:
        articles_qs = articles_qs.filter(sentiment=sentiment_filter)
    
    if source_filter:
        articles_qs = articles_qs.filter(source_name=source_filter)
    
    sources = list(NewsArticle.objects.values_list('source_name', flat=True).distinct().order_by('source_name'))
    
    paginator = Paginator(articles_qs, 12)
    page = request.GET.get('page', 1)
    
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    
    stats = NewsArticle.objects.aggregate(
        positive=Count(Case(When(sentiment='Positive', then=1))),
        negative=Count(Case(When(sentiment='Negative', then=1))),
        neutral=Count(Case(When(sentiment='Neutral', then=1)))
    )
    
    last_updated = NewsArticle.objects.order_by('-updated_at').values('updated_at').first()
    latest_articles = list(NewsArticle.objects.order_by('-published_at')[:5])
    
    context = {
        'articles': articles,
        'total_count': NewsArticle.objects.count(),
        'search_term': search_term,
        'sentiment_filter': sentiment_filter,
        'source_filter': source_filter,
        'sources': sources,
        'stats': stats,
        'last_updated': last_updated['updated_at'] if last_updated else None,
        'latest_articles': latest_articles,
    }
    return render(request, 'news/home.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def api_fetch_news(request):
    """API endpoint to trigger news fetch (for cron jobs)."""
    try:
        from news.tasks import fetch_and_save_articles
        try:
            result = fetch_and_save_articles.delay()
            return JsonResponse({'status': 'queued', 'task_id': str(result)})
        except Exception:
            result = fetch_and_save_articles()
            return JsonResponse({'status': 'completed', 'result': result})
    except Exception as e:
        logger.error(f"Fetch API error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def handler404(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)