import pandas as pd
from textblob import TextBlob

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

def process_reviews(file_path):
    """
    Processes reviews from an Excel file and performs sentiment analysis.
    
    Parameters:
    file_path (str): The path to the Excel file.
    
    Returns:
    DataFrame: A DataFrame containing the original reviews and their sentiment scores.
    """
    df = pd.read_excel(file_path)
    
    # Print column names to help debug
    print(f"Columns in {file_path}: {df.columns.tolist()}")
    
    # Check if 'Review Text' column is present
    if 'Review Text' not in df.columns:
        raise KeyError(f"'Review Text' column not found in {file_path}. Please check the column names and update the script.")
    
    # Assuming the reviews are in a column named 'Review Text'
    df['Polarity'] = df['Review Text'].apply(lambda x: analyze_sentiment(str(x))[0])
    df['Subjectivity'] = df['Review Text'].apply(lambda x: analyze_sentiment(str(x))[1])
    
    return df

def main():
    # Path to the Excel file
    file_path = "F:/Projects/Intel/Reviews/amazon_reviews12DP.xlsx"
    
    try:
        reviews_df = process_reviews(file_path)
        # Save the DataFrame with sentiment scores to a new Excel file
        reviews_df.to_excel("single_file_sentiment_analysis_results.xlsx", index=False)
        print(f"Sentiment analysis completed and results saved to 'single_file_sentiment_analysis_results.xlsx'.")
    except KeyError as e:
        print(e)

if __name__ == "__main__":
    main()
