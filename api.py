from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import (
    get_news_articles,
    analyze_sentiment,
    generate_hindi_tts,
    perform_comparative_analysis
)

app = FastAPI()

class NewsRequest(BaseModel):
    company_name: str

class TTSRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "News Summarization and TTS API is running!"}

@app.post("/extract-news/")
async def extract_news_api(request: NewsRequest):
    """Extracts news articles for the given company."""
    try:
        articles = get_news_articles(request.company_name)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        return {"company": request.company_name, "articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.post("/analyze-sentiment/")
async def analyze_sentiment_api(request: NewsRequest):
    """Performs sentiment analysis on extracted articles."""
    try:
        articles = get_news_articles(request.company_name)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        sentiment_report = analyze_sentiment(articles)
        return {"company": request.company_name, "sentiment_report": sentiment_report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

@app.post("/comparative-analysis/")
async def comparative_analysis_api(request: NewsRequest):
    """Performs a comparative sentiment analysis across multiple articles."""
    try:
        articles = get_news_articles(request.company_name)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        sentiment_report = analyze_sentiment(articles)
        comparison_report = perform_comparative_analysis(sentiment_report)
        return {"company": request.company_name, "comparative_analysis": comparison_report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing comparative analysis: {str(e)}")

@app.post("/generate-tts/")
async def generate_tts_api(request: TTSRequest):
    """Generates Hindi TTS from the provided text."""
    try:
        audio_path = generate_hindi_tts(request.text)
        if not audio_path:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        return {"audio_path": audio_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating TTS: {str(e)}")
