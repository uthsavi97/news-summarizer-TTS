from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import get_news_articles, analyze_sentiment, generate_hindi_tts


app = FastAPI()

class NewsRequest(BaseModel):
    company_name: str

@app.post("/extract-news/")
async def extract_news_api(request: NewsRequest):
    try:
        articles = get_news_articles(request.company_name)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        return {"company": request.company_name, "articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.post("/analyze-sentiment/")
async def analyze_sentiment_api(request: NewsRequest):
    try:
        articles = get_news_articles(request.company_name)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        sentiment_report = analyze_sentiment(articles)
        return {"company": request.company_name, "sentiment_report": sentiment_report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

class TTSRequest(BaseModel):
    text: str

@app.post("/generate-tts/")
async def generate_tts_api(request: TTSRequest):
    try:
        audio_path = generate_hindi_tts(request.text)
        if not audio_path:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        return {"audio_path": audio_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating TTS: {str(e)}")

@app.get("/")
def root():
    return {"message": "API is running!"}
