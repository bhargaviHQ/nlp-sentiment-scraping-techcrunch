from nltk.corpus import stopwords
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import langid
import pycountry
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi


# Load environment variables from .env file
load_dotenv()

df = pd.read_csv('merged_articles.csv')
num_rows = df.shape[0]
print(f'The number of rows in the CSV file is: {num_rows}')

# Download the stopwords dataset
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('punkt_tab')


def count_words_without_stopwords(text):
    if isinstance(text, (str, bytes)):
        words = nltk.word_tokenize(str(text))
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return len(filtered_words)
    else:
        0

df['Word Count'] = df['Article Content'].apply(count_words_without_stopwords)


sid = SentimentIntensityAnalyzer()

def get_sentiment(row):
    sentiment_scores = sid.polarity_scores(row)
    compound_score = sentiment_scores['compound']

    if compound_score >= 0.05:
        sentiment = 'Positive'
    elif compound_score <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return sentiment, compound_score

df[['Sentiment', 'Compound Score']] = df['Article Content'].astype(str).apply(lambda x: pd.Series(get_sentiment(x)))

def detect_language(text):
    # Convert NaN to an empty string
    text = str(text) if pd.notna(text) else ''
    
    # Use langid to detect the language
    lang, confidence = langid.classify(text)
    return lang

df['Language'] = df['Article Content'].apply(detect_language)
df['Language'] = df['Language'].map(lambda code: pycountry.languages.get(alpha_2=code).name if pycountry.languages.get(alpha_2=code) else code)

uri = os.environ['URI_KEY']

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Specify the database and collection
db = client['my_database']  # Create/use 'my_database'
collection = db['article_collection']  # Create/use 'my_collection'

# Convert DataFrame to dictionary (list of dictionaries)
data = df.to_dict(orient='records')

# Insert the data into the MongoDB collection
result = collection.insert_many(data)

# Print the inserted IDs
print("Inserted document IDs:", result.inserted_ids)

# Step 1: Identify duplicates
pipeline = [
    {
        "$group": {
            "_id": "$Link",  # Field to check for duplicates
            "uniqueIds": { "$addToSet": "$_id" },  # Store all unique _ids
            "count": { "$sum": 1 }  # Count duplicates
        }
    },
    {
        "$match": {
            "count": { "$gt": 1 }  # Only keep duplicates
        }
    }
]

duplicates = collection.aggregate(pipeline)

# Step 2: Remove duplicates
for doc in duplicates:
    unique_ids = doc['uniqueIds']
    unique_ids.pop(0)  # Keep the first id
    # Delete the duplicates
    collection.delete_many({"_id": {"$in": unique_ids}})

print("Duplicates removed.")