import csv
import logging
import os
import random
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import Settings
from cache_translator import CachedTranslator
from logger import setup_logging

# Setup logging
settings = Settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

# Free translator with cache
translator = CachedTranslator(settings.translation_cache)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0 Safari/537.36",
]


def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }


def scrape_reviews(product_url, num_reviews=50):
    session = requests.Session()
    retry = Retry(
        total=settings.max_retries,
        backoff_factor=settings.backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    reviews = []
    seen = set()
    page = 1

    while len(reviews) < num_reviews:
        try:
            response = session.get(
                product_url,
                headers=get_headers(),
                params={"pageNumber": page},
                timeout=settings.request_timeout,
            )
            response.raise_for_status()
        except Exception as e:
            logger.warning("Failed to fetch page %s: %s", page, e)
            break

        soup = BeautifulSoup(response.text, "html.parser")

        if page == 1:
            try:
                product_name = soup.find("span", {"id": "productTitle"}).text.strip()
            except AttributeError:
                product_name = "Product Name Not Found"

            try:
                price = soup.find("span", {"class": "a-price"}).text.strip()
            except AttributeError:
                price = "Price Not Found"

        review_elements = soup.find_all("div", {"data-hook": "review"})
        if not review_elements:
            logger.info("No reviews found on page %s", page)
            break

        for review in review_elements:
            try:
                reviewer = review.find("span", {"class": "a-profile-name"}).text.strip()
            except AttributeError:
                reviewer = "Anonymous"

            try:
                rating = review.find("i", {"data-hook": "review-star-rating"}).text.split(" ")[0]
            except AttributeError:
                rating = "N/A"

            try:
                review_text = review.find("span", {"data-hook": "review-body"}).text.strip()
            except AttributeError:
                review_text = "No review text"

            translated = translator.translate(review_text)

            dedup_key = (reviewer, rating, translated[:200])
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            reviews.append({
                "Product Name": product_name,
                "Price": price,
                "Reviewer": reviewer,
                "Rating": rating,
                "Review Text": translated,
            })

            if len(reviews) >= num_reviews:
                break

        page += 1
        time.sleep(settings.rate_limit_seconds)

    return reviews


def main():
    all_reviews = []
    for url in settings.product_urls:
        logger.info("Scraping %s", url)
        reviews = scrape_reviews(url, num_reviews=settings.num_reviews)
        all_reviews.extend(reviews)

    csv_file = settings.raw_csv
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["Product Name", "Price", "Reviewer", "Rating", "Review Text"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(all_reviews)

    logger.info("Reviews appended to %s", csv_file)


if __name__ == "__main__":
    main()