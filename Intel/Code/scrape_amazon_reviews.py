import requests
from bs4 import BeautifulSoup
from translate import Translator # type: ignore
import csv
import os

# Replace with your ScraperAPI key
API_KEY = 'YOUR API'

# Initialize Translator for US English
translator = Translator(to_lang="en")

def translate_to_us_english(text):
    try:
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Translation failed for: {text}")
        return text  # Return original text if translation fails

# Function to scrape reviews for a given product URL
def scrape_reviews(product_url, num_reviews=50):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    reviews = []
    page = 1

    while len(reviews) < num_reviews:
        response = requests.get(f'http://api.scraperapi.com?api_key={API_KEY}&url={product_url}&pageNumber={page}', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product details (only once for the first page)
        if page == 1:
            try:
                product_name = soup.find('span', {'id': 'productTitle'}).text.strip()
            except AttributeError:
                product_name = 'Product Name Not Found'

            try:
                price = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()
            except AttributeError:
                price = 'Price Not Found'

        # Extract review details
        review_elements = soup.find_all('div', {'data-hook': 'review'})
        if not review_elements:
            break

        for review in review_elements:
            try:
                reviewer = review.find('span', {'class': 'a-profile-name'}).text.strip()
            except AttributeError:
                reviewer = 'Anonymous'  # Handle cases where reviewer name is not found

            try:
                rating = review.find('i', {'data-hook': 'review-star-rating'}).text.split(' ')[0]
            except AttributeError:
                rating = 'N/A'  # Handle cases where rating is not found or is not available

            try:
                review_text = review.find('span', {'data-hook': 'review-body'}).text.strip()
                translated_review_text = translate_to_us_english(review_text)
            except AttributeError:
                review_text = 'No review text'  # Handle cases where review text is not found
                translated_review_text = 'No review text'

            reviews.append({
                'Product Name': product_name,
                'Price': price,
                'Reviewer': reviewer,
                'Rating': rating,
                'Review Text': translated_review_text
            })

            # Stop if we have enough reviews
            if len(reviews) >= num_reviews:
                break

        page += 1

    return reviews

def main():
    # List of product URLs (replace with actual Amazon product URLs)
    product_urls = [
        'place url' #Place your relevant URL
    ]

    all_reviews = []

    for url in product_urls:
        reviews = scrape_reviews(url, num_reviews=50)
        all_reviews.extend(reviews)

    csv_file = 'amazon_reviews12MP.csv'
    file_exists = os.path.isfile(csv_file)

    # Write reviews to a CSV file (append mode)
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['Product Name', 'Price', 'Reviewer', 'Rating', 'Review Text']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if the file is new
        if not file_exists:
            writer.writeheader()

        writer.writerows(all_reviews)

    print(f'Reviews appended to {csv_file}')

if __name__ == '__main__':
    main()
