# Generated migration to add created_at field

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_newsarticle_sentiment_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
    ]
