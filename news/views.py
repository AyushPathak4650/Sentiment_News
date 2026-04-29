from django.shortcuts import render
from .models import NewsArticle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.db.models.functions import TruncHour
from django.http import Http404
from django.utils import timezone


def dashboard(request):
    """Dashboard with sentiment stats and filtered articles."""
    search_term = request.GET.get('q', '')
    
    articles_qs = NewsArticle.objects.all().order_by('-published_at')
    
    if search_term:
        articles_qs = articles_qs.filter(
            Q(title__icontains=search_term) | 
            Q(description__icontains=search_term) |
            Q(source_name__icontains=search_term)
        )
    
    # Limit to 1000 articles for performance, then get top 100 for stats
    latest_100 = list(articles_qs[:1000][:100])
    
    stats = {'positive': 0, 'negative': 0, 'neutral': 0}
    for article in latest_100:
        if article.sentiment == 'Positive':
            stats['positive'] += 1
        elif article.sentiment == 'Negative':
            stats['negative'] += 1
        else:
            stats['neutral'] += 1
    
    # Get top sources
    sources = list(NewsArticle.objects.values('source_name').annotate(
        count=Count('id')
    ).order_by('-count')[:8])
    source_names = [s['source_name'] for s in sources]
    source_counts = [s['count'] for s in sources]
    
    # Get last fetch time
    last_article = NewsArticle.objects.order_by('-created_at').first()
    last_updated = last_article.created_at if last_article else None
    
    paginator = Paginator(latest_100, 9)
    page = request.GET.get('page', 1)
    
    try:
        articles = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        articles = paginator.page(1)
    
    context = {
        'articles': articles,
        'stats': stats,
        'search_term': search_term,
        'total_articles': NewsArticle.objects.count(),
        'source_names': source_names,
        'source_counts': source_counts,
        'last_updated': last_updated,
    }
    return render(request, 'news/dashboard.html', context)


def home(request):
    """Browse all articles with pagination."""
    articles_qs = NewsArticle.objects.all().order_by('-published_at')
    
    paginator = Paginator(articles_qs, 12)
    page = request.GET.get('page', 1)
    
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        # If page is too high, show last page
        articles = paginator.page(paginator.num_pages) if paginator.num_pages > 0 else paginator.page(1)
    
    context = {
        'articles': articles,
        'total_count': NewsArticle.objects.count(),
    }
    return render(request, 'news/home.html', context)


def handler404(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)