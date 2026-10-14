import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sentiment_category import categorize_polarity, analyze_sentiment


def test_categorize_very_negative():
    assert categorize_polarity(-0.8) == "Very Negative"


def test_categorize_negative():
    assert categorize_polarity(-0.2) == "Negative"


def test_categorize_neutral():
    assert categorize_polarity(0) == "Neutral"


def test_categorize_positive():
    assert categorize_polarity(0.3) == "Positive"


def test_categorize_very_positive():
    assert categorize_polarity(0.9) == "Very Positive"


def test_analyze_sentiment_returns_tuple():
    polarity, subjectivity = analyze_sentiment("This CPU is amazing!")
    assert isinstance(polarity, float)
    assert isinstance(subjectivity, float)