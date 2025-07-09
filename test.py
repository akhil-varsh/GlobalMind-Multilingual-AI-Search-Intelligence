import streamlit as st
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urlparse
import time

 # Your provided cx

def _get_language_restriction(language):
    # Map language to Google's language restriction format
    language_map = {
        "en": "lang_en",
        "hi": "lang_hi",
        "te": "lang_te",
        # Add more languages as needed
    }
    return language_map.get(language, "lang_en")  # Default to English

def google_search(query, api_key, cse_id, num_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": num_results,
        "lr": _get_language_restriction(language),  # Language restriction
        "gl": "IN",  # Geographic location: India
        "cr": "countryIN"  # Country restriction
    }
    st.write("Search Parameters Preview:")
    st.json(params)

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        st.error("Google Search API Error: " + response.text)
        return []



# 🖼️ Streamlit UI
st.title("🔍 Google CSE Real World Content Extractor")
query = st.text_input("Enter a search query (in Hindi, Telugu, etc.):")

if st.button("Search and Extract"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Searching..."):
            results = google_search(query, API_KEY, CSE_ID)


        if results:
            for item in results:
                title = item.get("title")
                link = item.get("link")

                # Show thumbnail if available
                image_url = item.get("pagemap", {}).get("cse_image", [{}])[0].get("src")
                if image_url:
                    st.image(image_url, caption=title, use_column_width=True)

                st.markdown(f"### [{title}]({link})")

                with st.spinner("Extracting content..."):
                    time.sleep(1)  # be nice to the server
                    article_title, article_text = extract_article_text(link)
                    st.markdown(f"**Extracted Title:** {article_title}")
                    st.markdown(f"**Content Preview:**\n\n{article_text[:1000]}...")

                st.markdown("---")

        else:
            st.info("No results found or failed to fetch.")

st.markdown("---")
st.markdown("💡 Powered by Google CSE + Newspaper3k + Streamlit")

