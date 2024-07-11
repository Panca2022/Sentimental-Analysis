from googletrans import Translator
import pandas as pd

# Function to translate text using Google Translate API
def translate_text(text, src_lang='auto', dest_lang='en'):
    translator = Translator()
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated.text

# Function to translate a column in a dataframe
def translate_column(column, src_lang='auto', dest_lang='en'):
    translated_column = []
    for entry in column:
        translated_entry = translate_text(entry, src_lang, dest_lang)
        translated_column.append(translated_entry)
    return translated_column

# Example usage with a dataframe
# Assuming 'amazon_reviews13MP.csv' is your input CSV file and 'Review Text' is the column to translate
try:
    data = pd.read_csv('amazon_reviews12MP.csv', encoding='latin-1')  # Try different encodings here
except UnicodeDecodeError as e:
    print(f"UnicodeDecodeError: {e}")

column_name = 'Review Text'     # Replace with the actual column name to translate

# Translate the column
translated_column = translate_column(data[column_name])

# Replace the column with translated data
data[column_name] = translated_column

# Save the translated data to a new file or update existing file
data.to_csv('translated_data.csv', index=False, encoding='utf-8-sig')  # Use the same encoding for output

print('Translation complete. Saved to translated_data.csv')
