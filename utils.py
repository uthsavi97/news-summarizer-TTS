import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_news_articles(query, max_articles=10):
    """
    Fetch news articles for a given company name.

    Args:
        query (str): Company name to search for.
        max_articles (int): Number of articles to fetch.

    Returns:
        list: List of dictionaries containing title, summary, and metadata.
    """
    base_url = "https://www.google.com/search?q={query}+news&hl=en&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Format URL with query
    url = base_url.format(query=query.replace(' ', '+'))
    logging.info(f"Fetching news articles for: {query}")

    try:
        # Fetch the page
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.info("Page fetched successfully.")

        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        # Extract articles
        news_items = soup.find_all('div', class_='dbsr')
        for item in news_items[:max_articles]:
            title = item.find('div', class_='JheGif nDgy9d').text if item.find('div', class_='JheGif nDgy9d') else 'No Title'
            summary = item.find('div', class_='Y3v8qd').text if item.find('div', class_='Y3v8qd') else 'No Summary'
            link = item.a['href'] if item.a else 'No Link'
            source = item.find('div', class_='XTjFC WF4CUc').text if item.find('div', class_='XTjFC WF4CUc') else 'No Source'
            timestamp = item.find('span', class_='WG9SHc').text if item.find('span', class_='WG9SHc') else 'No Timestamp'

            articles.append({
                'title': title,
                'summary': summary,
                'link': link,
                'source': source,
                'timestamp': timestamp
            })

        if len(articles) < max_articles:
            logging.warning(f"Only {len(articles)} articles found.")
        else:
            logging.info(f"Fetched {len(articles)} articles.")

        return articles

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching news: {e}")
        return []

# Quick test
if __name__ == "__main__":
    company = input("Enter a company name: ")
    articles = get_news_articles(company)
    print(f"Found {len(articles)} articles.")
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   {article['summary']}")
        print(f"   Source: {article['source']} | {article['timestamp']}")
        print(f"   Link: {article['link']}\n") 

# Unit tests
def test_extract_news(max_articles=5):
    logging.info("Running unit tests...")
    test_query = "Tesla"
    articles = get_news_articles(test_query, max_articles=max_articles)
    
    assert isinstance(articles, list), "Output should be a list."
    assert len(articles) <= max_articles, f"Should fetch at most {max_articles} articles."

    for article in articles:
        assert 'title' in article and isinstance(article['title'], str), "Each article should have a title."
        assert 'summary' in article and isinstance(article['summary'], str), "Each article should have a summary."
        assert 'link' in article and isinstance(article['link'], str), "Each article should have a link."
        assert 'source' in article and isinstance(article['source'], str), "Each article should have a source."
        assert 'timestamp' in article and isinstance(article['timestamp'], str), "Each article should have a timestamp."

    logging.info("All tests passed!")

from textblob import TextBlob

def analyze_sentiment(articles):
    sentiment_report = []
    for article in articles:
        analysis = TextBlob(article['summary'])
        sentiment = 'positive' if analysis.sentiment.polarity > 0 else 'negative' if analysis.sentiment.polarity < 0 else 'neutral'
        sentiment_report.append({'title': article['title'], 'sentiment': sentiment})
    return sentiment_report

def generate_hindi_tts(text):
    # Your code here
    pass



# Run tests
if __name__ == "__main__":
    test_extract_news()

