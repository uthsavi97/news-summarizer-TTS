import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from gtts import gTTS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Function to extract news articles
def extract_articles(company_name, num_articles=10):
    search_url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={API_KEY}"
    response = requests.get(search_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch news articles")

    data = response.json()
    articles = []
    for item in data.get("articles", [])[:num_articles]:
        title = item.get("title", "No Title")
        content = item.get("content", "No Content")
        url = item.get("url")
        articles.append({"title": title, "content": content, "url": url})
    return articles

# Function to summarize content
def summarize_content(content, max_sentences=3):
    sentences = content.split('.')
    return '. '.join(sentences[:max_sentences]) + '.' if sentences else content

# Function to extract key topics
def extract_topics(content):
    blob = TextBlob(content)
    nouns = [word for word, tag in blob.tags if tag == 'NN']
    return list(set(nouns))

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to perform comparative analysis
def comparative_analysis(articles):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment = analyze_sentiment(article['content'])
        sentiment_counts[sentiment] += 1
    return sentiment_counts

# Function to generate Hindi TTS
def generate_hindi_tts(text, output_path="output_hindi.mp3"):
    tts = gTTS(text=text, lang='hi')
    tts.save(output_path)
    return output_path
