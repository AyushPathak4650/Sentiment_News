from django.urls import path
import news.views as view

urlpatterns = [
    path('', view.home, name='news-home'),
    path('api/fetch/', view.api_fetch_news, name='api-fetch'),
]