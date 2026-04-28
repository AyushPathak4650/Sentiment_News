from django.contrib import admin
from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source_name', 'published_at', 'sentiment', 'sentiment_score', 'url')
    search_fields = ('title', 'description', 'source_name')
    list_filter = ('sentiment', 'published_at', 'source_name')
    readonly_fields = ('url', 'published_at', 'sentiment_score')
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)

    fieldsets = (
        ('Article Info', {
            'fields': ('title', 'description', 'url', 'source_name', 'image_url')
        }),
        ('Metadata', {
            'fields': ('published_at', 'sentiment', 'sentiment_score')
        }),
    )