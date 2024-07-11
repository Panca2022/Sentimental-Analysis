import pandas as pd
from textblob import TextBlob
import glob

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using TextBlob.
    
    Parameters:
    text (str): The text to analyze.
    
    Returns:
    tuple: Polarity and subjectivity of the text.
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity

def categorize_polarity(polarity):
    """
    Categorizes polarity into sentiment categories.
    
    Parameters:
    polarity (float): The polarity score.
    
    Returns:
    str: Sentiment category ('Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive').
    """
    if polarity < -0.5:
        return 'Very Negative'
    elif -0.5 <= polarity < 0:
        return 'Negative'
    elif polarity == 0:
        return 'Neutral'
    elif 0 < polarity <= 0.5:
        return 'Positive'
    elif polarity > 0.5:
        return 'Very Positive'
    else:
        return 'Undefined'

def process_reviews(file_path):
    """
    Processes reviews from an Excel file and performs sentiment analysis.
    
    Parameters:
    file_path (str): The path to the Excel file.
    
    Returns:
    DataFrame: A DataFrame containing the original reviews, their sentiment scores, and sentiment categories.
    """
    df = pd.read_excel(file_path)
    
    # Ensure the correct column name for reviews ('Review Text')
    if 'Review Text' in df.columns:
        df['Polarity'], df['Subjectivity'] = zip(*df['Review Text'].apply(lambda x: analyze_sentiment(str(x))))
    else:
        raise KeyError("'Review Text' column not found in {}".format(file_path))
    
    # Categorize polarity
    df['Polarity Category'] = df['Polarity'].apply(categorize_polarity)
    
    return df

def main():
    # Path to the directory containing the Excel files
    files = glob.glob(r"F:\Projects\Intel\Reviews\*.xlsx")
    
    all_reviews = []
    
    for file in files:
        try:
            reviews_df = process_reviews(file)
            all_reviews.append(reviews_df)
            print(f"Processed {file}")
        except KeyError as e:
            print(f"Error processing {file}: {str(e)}")
            continue
    
    if all_reviews:
        # Combine all DataFrames into a single DataFrame
        combined_reviews = pd.concat(all_reviews, ignore_index=True)
        
        # Save the combined DataFrame with sentiment scores to a new Excel file
        combined_reviews.to_excel("sentiment_analysis_results.xlsx", index=False)
        
        print("Sentiment analysis completed and results saved to 'sentiment_analysis_results.xlsx'.")
    else:
        print("No valid reviews found to process.")

if __name__ == "__main__":
    main()
