import requests
import time # Time is no longer needed for waiting for JS, but kept for consistency
from bs4 import BeautifulSoup
from typing import List

# --- Configuration (Move to your Streamlit app.py) ---
# It's crucial to set a User-Agent to mimic a real browser for basic anti-bot bypass.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# --- 1. CORE SCRAPING FUNCTION (Replaced Selenium) ---

def scrape_website(website: str) -> str:
    
    print(f"Attempting to fetch URL: {website}")
    
    try:
        # Use a timeout to prevent endless hanging
        response = requests.get(website, headers=HEADERS, timeout=15)
        
        # Raise an exception for HTTP errors (4xx or 5xx status codes)
        response.raise_for_status() 
        
        print("Page fetched successfully.")
        
        # You may still use a small delay if needed, but it's not strictly necessary here
        time.sleep(1) 
        
        return response.text
        
    except requests.exceptions.RequestException as e:
        # Log the detailed error
        print(f"Scraping failed for {website}. Error: {e}")
        # Return an empty string if scraping fails
        return ""

# --- 2. HTML PROCESSING FUNCTIONS (Optimized BeautifulSoup) ---

def extract_body_content(html_content: str) -> str:
    """Extracts the entire <body> tag content from the HTML."""
    if not html_content:
        return ""

    # Using the standard 'html.parser' is usually efficient enough
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.find('body')

    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content: str) -> str:
    """Removes scripts/styles and cleans up whitespace."""
    if not body_content:
        return ""
        
    soup = BeautifulSoup(body_content, "html.parser")

    # Efficiently extract script and style tags
    for script_or_style in soup(["script", "style", "noscript", "svg"]):
        script_or_style.extract()

    # Get text, using a single newline as a separator
    cleaned_content = soup.get_text(separator="\n")

    # Clean up excess whitespace and empty lines
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    return cleaned_content

# --- 3. CONTENT SPLITTING FUNCTION (Unchanged) ---

def split_dom_content(dom_content: str, max_length: int = 6000) -> List[str]:
    """Splits the large string into chunks of a maximum length."""
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]

# --- EXAMPLE USAGE (For Testing) ---
if __name__ == '__main__':
    test_url = "https://en.wikipedia.org/wiki/Web_scraping"
    
    html = scrape_website(test_url)

    if html:
        body_html = extract_body_content(html)
        cleaned_text = clean_body_content(body_html)
        
        # print("\n--- Cleaned Text Sample (First 500 chars) ---")
        # print(cleaned_text[:500])
        
        chunks = split_dom_content(cleaned_text)
        print(f"\n--- Content split into {len(chunks)} chunks. ---")
        # print(f"First chunk length: {len(chunks[0])}")
    else:
        print("Cannot proceed with extraction. HTML content is empty.")