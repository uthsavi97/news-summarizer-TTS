import streamlit as st
import requests
import os

# App title and description
st.title("News Summarizer and TTS")
st.write("Enter a company name to fetch recent news, analyze sentiment, and generate Hindi audio summaries.")

# Input for the company name
company_name = st.text_input("Enter Company Name:")

# Fetch data when company name is entered
if company_name:
    with st.spinner("Fetching news..."):
        response = requests.get(f"http://127.0.0.1:8000/news/{company_name}")
        if response.status_code == 200:
            st.session_state.news_data = response.json()
        else:
            st.error("Failed to fetch news. Please try again.")

# Check if data is fetched
if 'news_data' in st.session_state:
    data = st.session_state.news_data

    if 'Articles' in data:
        st.subheader("News Articles")
        for idx, article in enumerate(data['Articles']):
            st.write(f"**{idx + 1}. {article['Title']}**")
            st.write(f"Summary: {article['Summary']}")
            st.write(f"Sentiment: {article['Sentiment']}")
            st.write(f"Topics: {', '.join(article['Topics'])}")
            st.write("---")

        # Comparative Analysis
        st.subheader("Comparative Sentiment Analysis")
        sentiment_dist = data['Comparative Sentiment Score']['Sentiment Distribution']
        st.write(f"Positive: {sentiment_dist['Positive']} | Negative: {sentiment_dist['Negative']} | Neutral: {sentiment_dist['Neutral']}")

        for comp in data['Comparative Sentiment Score']['Coverage Differences']:
            st.write(f"- {comp['Comparison']}")
            st.write(f"Impact: {comp['Impact']}")

        # Final Sentiment Analysis
        st.subheader("Final Sentiment Analysis")
        st.write(data['Final Sentiment Analysis'])

        # Audio Generation
        st.subheader("Hindi Text-to-Speech")
        audio_response = requests.get(f"http://127.0.0.1:8000/tts/{company_name}")
        if audio_response.status_code == 200:
            audio_path = "tts_output.mp3"
            with open(audio_path, "wb") as f:
                f.write(audio_response.content)
            st.audio(audio_path)
        else:
            st.error("Failed to generate Hindi audio. Please try again.")
    else:
        st.error("No articles found. Please check the company name.")
