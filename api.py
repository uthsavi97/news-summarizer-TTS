from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from utils import extract_articles, comparative_analysis, generate_hindi_tts
import uvicorn

app = FastAPI()

# Request model
class CompanyRequest(BaseModel):
    company_name: str
    num_articles: int = 10

# Response model
class AnalysisResponse(BaseModel):
    company: str
    articles: list
    comparative_sentiment: dict
    topics: list
    audio_path: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "News Analysis API is running"}

# Extract Articles
@app.post("/extract_articles/")
def get_articles(request: CompanyRequest):
    try:
        articles = extract_articles(request.company_name, request.num_articles)
        return {"company": request.company_name, "articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Perform Sentiment and Comparative Analysis
@app.post("/analyze_sentiment/")
def analyze_articles(request: CompanyRequest):
    try:
        articles = extract_articles(request.company_name, request.num_articles)
        sentiment_counts, topics = comparative_analysis(articles)
        audio_path = generate_hindi_tts(f"{request.company_name} ke news ka vishleshan safalta purvak pura hua.")
        return AnalysisResponse(company=request.company_name, articles=articles, comparative_sentiment=sentiment_counts, topics=topics, audio_path=audio_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)