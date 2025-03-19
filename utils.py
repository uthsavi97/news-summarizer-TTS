import requests
from newspaper import Article
from textblob import TextBlob
import pyttsx3

# Function to extract news article text
def extract_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error extracting article: {e}")
        return None

# Function to analyze sentiment
def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        sentiment = blob.sentiment
        return sentiment.polarity, sentiment.subjectivity
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None, None

# Function to generate text-to-speech (TTS)
def generate_tts(text, output_file="output.mp3"):
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        print(f"Audio saved as {output_file}")
    except Exception as e:
        print(f"Error generating TTS: {e}")

# Example usage
if __name__ == "__main__":
    url = input("Enter the news article URL: ")
    article_text = extract_article_text(url)
    
    if article_text:
        polarity, subjectivity = analyze_sentiment(article_text)
        print(f"Sentiment Polarity: {polarity}, Subjectivity: {subjectivity}")
        generate_tts(article_text)
