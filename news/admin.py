from django.contrib import admin
from .models import NewsArticle

# Register your models here.
@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source_name', 'published_at', 'sentiment')
    search_fields = ('title', 'source_name', 'sentiment')
    list_filter = ('sentiment', 'published_at')