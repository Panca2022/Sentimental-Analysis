import glob
import logging
import os

import pandas as pd
from textblob import TextBlob

from config import Settings
from data_validation import validate_reviews
from logger import setup_logging

settings = Settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


def analyze_sentiment(text):
    blob = TextBlob(str(text))
    return blob.sentiment.polarity, blob.sentiment.subjectivity


def categorize_polarity(polarity):
    if polarity < -0.5:
        return "Very Negative"
    elif -0.5 <= polarity < 0:
        return "Negative"
    elif polarity == 0:
        return "Neutral"
    elif 0 < polarity <= 0.5:
        return "Positive"
    elif polarity > 0.5:
        return "Very Positive"
    else:
        return "Undefined"


def process_reviews(file_path):
    df = pd.read_excel(file_path)

    if "Review Text" not in df.columns:
        raise KeyError(f"'Review Text' column not found in {file_path}")

    # Clean and validate
    df = validate_reviews(df)

    # Sentiment analysis
    df["Polarity"], df["Subjectivity"] = zip(
        *df["Review Text"].apply(lambda x: analyze_sentiment(x))
    )
    df["Polarity Category"] = df["Polarity"].apply(categorize_polarity)

    return df


def main():
    # Use a configurable input folder. Default: data/raw
    input_dir = os.getenv("INPUT_DIR", "data/raw")
    files = glob.glob(os.path.join(input_dir, "*.xlsx"))

    if not files:
        logger.warning("No Excel files found in %s", input_dir)
        return

    all_reviews = []
    for file in files:
        try:
            reviews_df = process_reviews(file)
            all_reviews.append(reviews_df)
            logger.info("Processed %s", file)
        except Exception as e:
            logger.error("Error processing %s: %s", file, e)

    if all_reviews:
        combined = pd.concat(all_reviews, ignore_index=True)
        output_path = settings.processed_csv
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        combined.to_excel(output_path, index=False)
        logger.info("Sentiment analysis completed. Saved to %s", output_path)
    else:
        logger.warning("No valid reviews found to process.")


if __name__ == "__main__":
    main()