from django.urls import path
import news.views as view

# Home page for the news app
urlpatterns = [
    path('', view.home, name='news-home'),
]