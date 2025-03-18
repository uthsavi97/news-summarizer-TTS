# News Summarizer with Text-to-Speech (TTS)

This project is a web application that fetches the latest news about a given company, summarizes the articles, and converts the summary into speech. Built with FastAPI for the backend and Streamlit for the frontend.

## Features
- Fetches the latest news articles for a given company
- Summarizes the news content
- Converts the summary to speech
- Simple web interface using Streamlit

## Technologies Used
- Python
- FastAPI
- Streamlit
- Requests
- gTTS (Google Text-to-Speech)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/news-summarizer-tts.git
   cd news-summarizer-tts
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate    # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup
1. Obtain an API key from [News API](https://newsapi.org/).
2. Create a `.env` file in the project root and add your API key:
   ```plaintext
   NEWS_API_KEY=your_api_key_here
   ```

## Running the Application
1. Start the FastAPI backend:
   ```bash
   uvicorn api:app --reload
   ```
2. Start the Streamlit frontend:
   ```bash
   streamlit run app.py
   ```

The frontend will be available at: [http://localhost:8501](http://localhost:8501)

## API Endpoints
- **GET /**: Health check
- **POST /summarize**: Fetches and summarizes news articles
  - **Request Body:**
    ```json
    {
      "company": "Tesla"
    }
    ```
  - **Response:**
    ```json
    {
      "summary": "Tesla reported record profits..."
    }
    ```

## Deployment (Hugging Face Spaces)
1. Create a new Space on Hugging Face.
2. Set the Space SDK to **Streamlit**.
3. Push your code to the Space:
   ```bash
   git remote add origin https://huggingface.co/spaces/yourusername/news-summarizer-tts
   git push origin main
   ```
4. Your app will be deployed automatically.

## License
This project is licensed under the MIT License.

---
