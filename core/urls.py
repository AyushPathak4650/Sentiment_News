from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.core.cache import cache
from news.tasks import fetch_and_save_articles
import news.views
import time

RATE_LIMIT_SECONDS = 300

def api_fetch(request):
    if request.method == 'POST':
        # Verify API key (required)
        api_key = request.POST.get('key') or request.GET.get('key')
        expected_key = getattr(settings, 'FETCH_API_KEY', None)
        if not expected_key or api_key != expected_key:
            return JsonResponse({'error': 'Unauthorized - API key required'}, status=401)
        
        try:
            last_fetch = cache.get('last_fetch_time', 0)
            if time.time() - last_fetch < RATE_LIMIT_SECONDS:
                remaining = RATE_LIMIT_SECONDS - int(time.time() - last_fetch)
                return JsonResponse({'error': f'Rate limited. Try again in {remaining}s'}, status=429)
            
            cache.set('last_fetch_time', time.time())
        except Exception as e:
            # Proceed even if cache fails
            pass
        
        try:
            result = fetch_and_save_articles.delay()
            return JsonResponse({'status': 'started', 'task_id': result.id})
        except Exception as e:
            return JsonResponse({'error': f'Failed to start task: {str(e)}'}, status=500)
    return JsonResponse({'error': 'POST required'}, status=405)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', news.views.dashboard, name='dashboard'),
    path('news/', include('news.urls')),
    path('api/fetch/', api_fetch, name='api-fetch'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)