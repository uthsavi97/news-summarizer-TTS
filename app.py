import streamlit as st
import requests
import os

# Backend URL
API_URL = "http://127.0.0.1:8000"

st.title("News Summarization and Sentiment Analysis")
st.write("Enter a company name to get recent news articles, analyze sentiments, and listen to the summary in Hindi.")

# Input Section
company = st.text_input("Enter Company Name:", "Tesla")

if st.button("Analyze News"):
    with st.spinner("Fetching articles..."):
        response = requests.get(f"{API_URL}/extract_articles/?company_name={company}")
        if response.status_code != 200:
            st.error("Failed to fetch articles")
        else:
            articles = response.json()
            st.success("Articles Fetched!")

            # Display Articles
            for article in articles:
                st.subheader(article['title'])
                st.write(article['content'][:500] + "...")  # Show a preview
                st.write(f"[Read More]({article['url']})")

            # Sentiment Analysis
            with st.spinner("Analyzing sentiments..."):
                analysis_response = requests.post(f"{API_URL}/analyze_sentiment/", json={"articles": articles})
                if analysis_response.status_code != 200:
                    st.error("Failed to analyze sentiments")
                else:
                    analysis = analysis_response.json()
                    st.success("Sentiments Analyzed!")

                    st.write("### Comparative Sentiment Analysis")
                    st.write(analysis["sentiment_counts"])
                    st.write("### Topics")
                    st.write(analysis["topics"])
                    st.write("### Hindi Audio Summary")
                    audio_path = analysis.get("audio_path")
                    if audio_path and os.path.exists(audio_path):
                        st.audio(audio_path)
                    else:
                        st.warning("No audio generated.")

st.write("Developed by Uthsavi YP")