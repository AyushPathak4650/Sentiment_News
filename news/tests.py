from django.test import TestCase
from news.helpers import analyze_sentiment, POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS


class SentimentAnalysisTestCase(TestCase):
    """Test cases for sentiment analysis."""

    def test_positive_sentiment(self):
        """Test positive sentiment detection."""
        result, score = analyze_sentiment("Stock market surges to record high with strong gains")
        self.assertEqual(result, "Positive")

    def test_negative_sentiment(self):
        """Test negative sentiment detection."""
        result, score = analyze_sentiment("Market crashes as stocks plunge heavily")
        self.assertEqual(result, "Negative")

    def test_neutral_sentiment(self):
        """Test neutral sentiment detection."""
        result, score = analyze_sentiment("Company announces meeting")
        self.assertEqual(result, "Neutral")

    def test_empty_text(self):
        """Test empty text returns Neutral."""
        result, score = analyze_sentiment("")
        self.assertEqual(result, "Neutral")

    def test_none_text(self):
        """Test None text returns Neutral."""
        result, score = analyze_sentiment(None)
        self.assertEqual(result, "Neutral")

    def test_positive_keywords_included(self):
        """Verify positive keywords are defined."""
        self.assertIn('surge', POSITIVE_KEYWORDS)
        self.assertIn('success', POSITIVE_KEYWORDS)

    def test_negative_keywords_included(self):
        """Verify negative keywords are defined."""
        self.assertIn('crash', NEGATIVE_KEYWORDS)
        self.assertIn('loss', NEGATIVE_KEYWORDS)

    def test_negation_handling(self):
        """Test negation flips negative to less negative."""
        result, score = analyze_sentiment("Market did not crash today")
        self.assertIn(result, ['Neutral', 'Positive'])

    def test_long_text_truncation(self):
        """Test long text is handled properly."""
        long_text = "positive " * 1000
        result, score = analyze_sentiment(long_text)
        self.assertEqual(result, "Positive")

    def test_score_range(self):
        """Test score is in valid range."""
        result, score = analyze_sentiment("Stock market surges")
        self.assertGreaterEqual(score, -1.0)
        self.assertLessEqual(score, 1.0)