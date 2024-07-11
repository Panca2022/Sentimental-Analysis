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
    df['Sentiment Category'] = df['Polarity'].apply(categorize_polarity)
    
    return df[['Product Name', 'Price', 'Reviewer', 'Rating', 'Review Text', 'Polarity', 'Subjectivity', 'Sentiment Category']]

def main():
    # Specify the path to the Excel file
    file_path = r"F:\Projects\Intel\Reviews\amazon_reviews14.xlsx"
    
    try:
        reviews_df = process_reviews(file_path)
        
        # Save the DataFrame with sentiment scores and categories to a new Excel file
        reviews_df.to_excel("sentiment_analysis_single_file.xlsx", index=False)
        
        print(f"Sentiment analysis completed for '{file_path}' and results saved to 'sentiment_analysis_single_file.xlsx'.")
        
    except KeyError as e:
        print(f"Error processing {file_path}: {str(e)}")
    
if __name__ == "__main__":
    main()
