import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    raw_csv: str = os.getenv("RAW_CSV", "data/raw/amazon_reviews.csv")
    processed_csv: str = os.getenv("PROCESSED_CSV", "data/processed/sentiment_results.csv")
    output_dir: str = os.getenv("OUTPUT_DIR", "data/outputs")
    translation_cache: str = os.getenv("TRANSLATION_CACHE", "data/cache/translations.sqlite")
    num_reviews: int = int(os.getenv("NUM_REVIEWS", "50"))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "5"))
    backoff_factor: float = float(os.getenv("BACKOFF_FACTOR", "1.5"))
    rate_limit_seconds: float = float(os.getenv("RATE_LIMIT_SECONDS", "2.0"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    product_urls: list = field(default_factory=list)

    def __post_init__(self):
        if not self.product_urls:
            urls = os.getenv("PRODUCT_URLS", "")
            self.product_urls = [u.strip() for u in urls.split(",") if u.strip()]