from django.shortcuts import render
from .models import NewsArticle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404


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
    
    latest_100 = list(articles_qs[:100])
    
    stats = {'positive': 0, 'negative': 0, 'neutral': 0}
    for article in latest_100:
        if article.sentiment == 'Positive':
            stats['positive'] += 1
        elif article.sentiment == 'Negative':
            stats['negative'] += 1
        else:
            stats['neutral'] += 1
    
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
        articles = paginator.page(paginator.num_pages)
    
    context = {
        'articles': articles,
        'total_count': NewsArticle.objects.count(),
    }
    return render(request, 'news/home.html', context)


def handler404(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)