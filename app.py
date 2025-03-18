import streamlit as st
import requests

# Set up the Streamlit app
st.title("News Summarizer and TTS")

# Input for the company name
company_name = st.text_input("Enter Company Name:")

# Fetch news data when a company name is entered
if company_name:
    response = requests.get(f"http://127.0.0.1:8000/news/{company_name}")
    st.session_state.news_data = response.json()

    # Print API response to inspect the structure
    st.write("API Response:", st.session_state.news_data)

    # Check if 'articles' key exists in the response
    if 'articles' in st.session_state.news_data:
        st.write("News Articles")
        for idx, article in enumerate(st.session_state.news_data['articles']):
            st.write(f"{idx + 1}. {article['title']}")
    else:
        st.error("No articles found. Please check the company name or API response.")
