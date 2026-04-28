from django.db import models
from django.utils import timezone


class NewsArticle(models.Model):
    """News article model with sentiment analysis."""
    
    SENTIMENT_CHOICES = [
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('Neutral', 'Neutral'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(unique=True)
    source_name = models.CharField(max_length=100)
    published_at = models.DateTimeField()
    image_url = models.URLField(blank=True, null=True)
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, default='Neutral')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['sentiment']),
            models.Index(fields=['-updated_at']),
        ]

    def __str__(self):
        return self.title