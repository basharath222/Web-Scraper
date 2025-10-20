import streamlit as st
import scrape
import parse
import requests


st.title("AI Web Scraper")
url = st.text_input("Enter the URL of the webpage to scrape:")

if st.button("Scrape Site"):
    st.info("Scraping the website")
    try:
        result = scrape.scrape_website(url)
        if not result:
            st.error("Scraping Failed! This often means the URL is INVALID (typo) or the website immediately blocked the request.")
            st.stop()
            # print(result)
        body_content = scrape.extract_body_content(result)
        cleaned_content = scrape.clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content

        with st.expander("View DOM Content"):
            st.text_area("DOM Content",cleaned_content,height=300)
    except requests.exceptions.RequestException as e:
        st.error(f"Error scraping the website: {e}")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.info("Parsing the Content")

            dom_chunks = scrape.split_dom_content(st.session_state.dom_content)
            result = parse.parse_with_gemini(dom_chunks, parse_description)
            st.write(result)
