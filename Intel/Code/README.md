# Intel Processor Amazon Review Sentiment Analysis Pipeline

A free, Python-only, end-to-end data pipeline that scrapes Amazon customer reviews for Intel desktop and mobile processors, translates non-English reviews to English, performs sentiment analysis, categorises sentiment, and visualises the distribution — turning unstructured customer voice into decision-ready insights.

---

# Author

**Sri Hari Aravindan**

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Business Problem](#2-business-problem)
3. [Objectives](#3-objectives)
4. [Architecture](#4-architecture)
5. [Folder Structure](#5-folder-structure)
6. [Features](#6-features)
7. [How It Works](#7-how-it-works)
8. [Installation](#8-installation)
9. [Configuration](#9-configuration)
10. [Usage](#10-usage)
11. [Module Reference](#11-module-reference)
12. [Why These Design Decisions](#12-why-these-design-decisions)
13. [Reliability Engineering](#13-reliability-engineering)
14. [Testing](#14-testing)
15. [Docker](#15-docker)
16. [CI/CD](#16-cicd)
17. [Observations from the Data](#17-observations-from-the-data)
18. [Limitations](#18-limitations)
19. [Future Improvements](#19-future-improvements)
20. [Interview Notes](#20-interview-notes)

---

## 1. Project Overview

This project collects customer reviews from Amazon product pages for Intel processors (12th, 13th, and 14th Gen desktop and mobile CPUs), translates them into English, and performs automated sentiment analysis.

Each review receives:

- A **polarity score** (from -1.0 to 1.0)
- A **subjectivity score** (from 0.0 to 1.0)
- A **sentiment category** (Very Negative, Negative, Neutral, Positive, Very Positive)

The results are saved as Excel/CSV files and visualised as pie charts showing sentiment distribution per product category.

The pipeline is built entirely with free, open-source Python libraries. **No paid API is required.**

---

## 2. Business Problem

Amazon reviews contain valuable customer voice, but they are:

- **Unstructured** — free text with no fixed format
- **Multilingual** — reviews from many regions
- **High volume** — thousands of reviews per product
- **Mixed sentiment** — positive and negative in one review
- **Time-consuming** — impossible to read manually at scale

Manual analysis is slow, subjective, and cannot scale. Product and brand teams need an automated way to:

- Detect quality issues early
- Understand what customers praise and complain about
- Track sentiment across product generations
- Support data-driven product decisions

This project solves that by converting raw review text into measurable sentiment metrics.

---

## 3. Objectives

1. Scrape Amazon reviews for Intel processors using free tools.
2. Translate non-English reviews into English.
3. Perform sentiment analysis on each review.
4. Categorise sentiment into five levels.
5. Deduplicate and validate data for accuracy.
6. Save results to CSV and Excel.
7. Visualise sentiment distribution.
8. Make the pipeline portable, testable, and reproducible.

---

## 4. Architecture

```text
Amazon Product URL
        |
        v
[ Free Direct Scraper ]
  requests + BeautifulSoup (retry + rate limiting)
        |
        v
Raw Reviews (CSV)
        |
        v
[ Cached Translator ]
  deep-translator + SQLite cache
        |
        v
Translated Reviews
        |
        v
[ Data Validation ]
  remove empty rows + duplicates
        |
        v
[ Sentiment Analyzer ]
  TextBlob (polarity + subjectivity)
        |
        v
[ Sentiment Categorizer ]
  5-level classification
        |
        v
Excel / CSV Output
        |
        v
[ Visualisation ]
  matplotlib pie chart
```

Each stage is a separate module. This means any stage can be replaced without breaking the rest. For example, TextBlob can be swapped for VADER or a transformer model without touching the scraper.

---

## 5. Folder Structure

```text
Intel/Code/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
├── config.py
├── logger.py
├── cache_translator.py
├── data_validation.py
├── scrape_amazon_reviews.py
├── sentiment_category.py
├── sentiment_category_individual.py
├── analysis_review_text.py
├── creating_pie.py
├── tests/
│   └── test_sentiment.py
└── data/
    ├── raw/
    ├── processed/
    ├── cache/
    └── outputs/
```

---

## 6. Features

### Core Features

- Scrapes product name, price, reviewer, rating, and review text
- Translates reviews to English (free, cached)
- Computes polarity and subjectivity with TextBlob
- Categorises sentiment into 5 levels
- Removes empty reviews and duplicates
- Saves to CSV and Excel
- Generates pie charts

### Reliability Features

- Environment-based configuration (`.env`)
- Structured logging (`logger.py`)
- Retry with exponential backoff (`requests` Retry adapter)
- Rate limiting between requests
- Translation caching (SQLite)
- Data validation (`data_validation.py`)
- Modular architecture
- Unit tests with `pytest`
- Docker support
- GitHub Actions CI

---

## 7. How It Works

### Step 1 — Scraping

`scrape_amazon_reviews.py` sends GET requests directly to Amazon product pages using browser-like headers. It uses a `requests.Session` with a `Retry` adapter for automatic retries on `429/500/502/503/504` errors. Between pages, it waits `RATE_LIMIT_SECONDS` to avoid being blocked.

For each review, it extracts:

- Reviewer name
- Star rating
- Review text

### Step 2 — Translation

`cache_translator.py` checks an SQLite cache first. If the review text has been translated before, it returns the cached version. Otherwise, it calls `deep-translator` (a free Google Translate wrapper) and stores the result.

### Step 3 — Storage

Reviews are appended to a CSV file (`data/raw/amazon_reviews.csv`) with a header written only on the first run.

### Step 4 — Data Validation

`data_validation.py` checks that required columns exist, removes rows with empty review text, and removes duplicates based on `(Reviewer, Review Text)`.

### Step 5 — Sentiment Analysis

`sentiment_category.py` runs TextBlob on each review to compute:

- Polarity (-1 to +1)
- Subjectivity (0 to 1)

Then it applies `categorize_polarity()`:

| Polarity Range | Category      |
|----------------|---------------|
| `< -0.5`       | Very Negative |
| `-0.5 to < 0`  | Negative      |
| `== 0`         | Neutral       |
| `0 to <= 0.5`  | Positive      |
| `> 0.5`        | Very Positive |

### Step 6 — Output

The combined results are saved to Excel. A pie chart is generated with `matplotlib` showing the percentage of each sentiment category.

---

## 8. Installation

```bash
git clone <repo-url>
cd Intel/Code
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 9. Configuration

Copy `.env.example` to `.env` and edit:

```env
RAW_CSV=data/raw/amazon_reviews.csv
PROCESSED_CSV=data/processed/sentiment_results.csv
OUTPUT_DIR=data/outputs
TRANSLATION_CACHE=data/cache/translations.sqlite
INPUT_DIR=data/raw

PRODUCT_URLS=https://www.amazon.com/dp/PRODUCT_ID_1,https://www.amazon.com/dp/PRODUCT_ID_2
NUM_REVIEWS=50
REQUEST_TIMEOUT=30
MAX_RETRIES=5
BACKOFF_FACTOR=1.5
RATE_LIMIT_SECONDS=2.0

LOG_LEVEL=INFO
```

**Why `.env`?** It keeps secrets and machine-specific paths out of the code. This is standard for production systems and makes the project portable.

---

## 10. Usage

Scrape fresh reviews:

```bash
python scrape_amazon_reviews.py
```

Run sentiment analysis on all Excel files in `INPUT_DIR`:

```bash
python sentiment_category.py
```

Run sentiment analysis on a single file:

```bash
python sentiment_category_individual.py
```

Generate pie chart:

```bash
python creating_pie.py
```

---

## 11. Module Reference

| Module                             | Purpose                                  |
|------------------------------------|------------------------------------------|
| `config.py`                        | Loads settings from `.env`               |
| `logger.py`                        | Structured logging to console + file     |
| `cache_translator.py`              | Translates with SQLite cache             |
| `data_validation.py`               | Cleans and validates review DataFrame    |
| `scrape_amazon_reviews.py`         | Scrapes Amazon reviews                   |
| `sentiment_category.py`            | Sentiment analysis for all files         |
| `sentiment_category_individual.py` | Sentiment analysis for one file          |
| `analysis_review_text.py`          | Basic sentiment function only            |
| `creating_pie.py`                  | Generates pie chart                      |
| `tests/test_sentiment.py`          | Unit tests                               |

---

## 12. Why These Design Decisions

**Why modular architecture?**
Each stage (scraping, translation, sentiment, visualisation) is separate. If scraping breaks, sentiment still works on existing data. If we swap TextBlob for VADER, only one file changes.

**Why `.env` + `config.py`?**
Hardcoded paths like `F:/Projects/Intel/...` break on other machines. Environment variables make the project portable and safe (API keys not committed).

**Why retry + backoff?**
Scraping and translation are network operations. Temporary failures are normal. Retry with exponential backoff (wait 1s, then 2s, then 4s) handles them automatically.

**Why rate limiting?**
Sending requests too fast gets you blocked. A delay between requests is polite and safe.

**Why translation caching?**
Translation is slow and may fail. Caching means the same review is never translated twice. This makes repeated runs much faster.

**Why data validation?**
Bad data gives wrong sentiment. Duplicates skew charts. Empty rows crash TextBlob. Validation prevents all three.

**Why TextBlob?**
It is free, offline, and simple. Good for a prototype. For production, VADER or a transformer model gives better accuracy.

**Why logging instead of `print()`?**
`print()` disappears when code runs on a server. Logging writes to both the terminal and `pipeline.log`, so failures can be diagnosed later.

**Why tests?**
Tests prove the categorization logic works. They protect against future changes breaking existing behavior.

---

## 13. Reliability Engineering

| Feature    | Implementation                  | Why It Matters                       |
|------------|---------------------------------|--------------------------------------|
| Retry      | `urllib3.Retry` via `HTTPAdapter` | Handles transient network errors   |
| Backoff    | Exponential in `Retry`          | Avoids hammering a failing server    |
| Rate limit | `time.sleep()` between pages    | Avoids IP blocks                     |
| Cache      | SQLite table                    | Avoids duplicate translation work    |
| Dedup      | `(Reviewer, ReviewText)` key    | Prevents skewed sentiment charts     |
| Validation | `validate_reviews()`            | Removes garbage rows                 |
| Logging    | `logging` + file handler        | Debugging and audit trail            |
| Config     | `.env` file                     | Portability + secret safety          |
| Tests      | `pytest`                        | Prevents regressions                 |
| CI         | GitHub Actions                  | Automated quality gate               |

---

## 14. Testing

Run:

```bash
pytest -q
```

Tests cover:

- Each of the 5 sentiment categories
- Return type of `analyze_sentiment`

Example:

```python
def test_categorize_very_positive():
    assert categorize_polarity(0.9) == "Very Positive"
```

---

## 15. Docker

```bash
docker build -t intel-review-sentiment .
docker run --env-file .env intel-review-sentiment
```

**Why Docker?** It guarantees the same environment everywhere, removing the "works on my machine" problem.

---

## 16. CI/CD

`.github/workflows/ci.yml` runs tests on every push and pull request.

**Why?** Automated quality. Broken code never merges silently.

---

## 17. Observations from the Data

Most reviews for Intel 12th, 13th, and 14th Gen processors are **Positive** or **Very Positive**.

**Common positive themes:**

- Excellent value for money
- Strong gaming performance
- Good integrated graphics
- Efficient multitasking

**Common negative themes:**

- High heat under load
- Stock cooler insufficient
- Packaging problems
- Defective or used units from third-party sellers
- Price concerns for 14th Gen

Other observations:

- TextBlob sometimes misclassifies mixed reviews because it does not understand context well.
- Duplicate reviews are common in scraped Excel outputs — validation is essential.

---

## 18. Limitations

| Limitation                     | Impact                                       |
|--------------------------------|----------------------------------------------|
| Free scraping is fragile       | Amazon may block direct requests             |
| `deep-translator` is unofficial | May fail or rate-limit                      |
| TextBlob is a baseline model   | Lower accuracy than transformers             |
| No labeled ground truth        | Cannot compute precision/recall              |
| No database                    | Hard to query at scale                       |
| No dashboard                   | Non-technical users cannot explore           |

> **Note:** Free scraping of Amazon may violate their Terms of Service. For production, use the official Amazon Product Advertising API or a licensed dataset.

---

## 19. Future Improvements

1. **Better sentiment model** — Replace TextBlob with VADER + RoBERTa transformer.
2. **Aspect-based sentiment** — Extract sentiment per feature (performance, heat, price).
3. **Topic modelling** — LDA or BERTopic to discover themes automatically.
4. **Database** — Store in PostgreSQL for querying and joins.
5. **Dashboard** — Streamlit or Power BI for interactive exploration.
6. **Scheduled runs** — Cron or Airflow for continuous monitoring.
7. **Evaluation** — Label 200 reviews manually and compute F1 score.
8. **Multi-product comparison** — Compare sentiment across Intel generations and vs AMD.

---

## 20. Interview Notes

### Two-minute pitch

> "This project is an end-to-end sentiment analysis pipeline for Amazon reviews of Intel processors. It scrapes reviews, translates them, analyses sentiment, categorises it into five levels, and visualises the distribution. The prototype uses free Python libraries — requests, BeautifulSoup, deep-translator, TextBlob, pandas, and matplotlib.
>
> To make it reliable, I added environment-based configuration, structured logging, retry with backoff, rate limiting, translation caching, data validation, unit tests, Docker, and CI. It runs on any machine, handles failures gracefully, and removes duplicates that would otherwise skew insights.
>
> For a consumer goods company, this type of pipeline turns customer voice into measurable sentiment — useful for brand health monitoring, product quality detection, and data-driven decisions."

### Honest framing

> "The prototype uses free tools. For production, I would replace free scraping and translation with official APIs or licensed data, and upgrade sentiment to a transformer model. But the architecture already supports this swap because it's modular."

---

Built as a data engineering and NLP portfolio project demonstrating:

**ETL pipeline design · API integration · Translation · Sentiment analysis · Data validation · Reliability engineering · Testing · CI/CD · Business insight generation**