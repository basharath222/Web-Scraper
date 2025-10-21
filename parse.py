import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# load the environment variables from .env
# load_dotenv()

# Get the key from the environment
google_api_key = st.secrets["GEMINI_API_KEY"]

os.environ["GOOGLE_API_KEY"] = google_api_key

if not google_api_key:
    raise ValueError("!!!Gemini API key not found! Please check your Streamlit Secrets!!!")

# 🔹 Prompt Template
template = (
    "**ROLE:** You are an expert **Data Extraction Engine**. Your sole purpose is to process raw web content and deliver structured data with 100% fidelity to the user's instructions. You are extremely strict about output format."
"\n\n"
"**INPUT CONTENT:**\n"
"--- START OF DOCUMENT ---\n"
"{dom_content}\n"
"--- END OF DOCUMENT ---\n"
"\n"
"**EXTRACTION GOAL:** Extract the exact data points that match this description: {parse_description}."
"\n\n"
"**INSTRUCTIONS:**"
"\n"
"1.  **Mandatory Compliance:** The output *must* contain **only** the requested data. Do not use markdown (like '```json' or '```text'), quotes, or any surrounding text. 🚫"
"2.  **Formatting Rule:** If the goal is to extract multiple pieces of data, place **each extracted item on a new line** (delimited by '\\n')."
"3.  **No Match Rule:** If, and only if, absolutely **no** information matching the description is found in the document, you must return an **empty string** ('') and nothing else. 🤫"
"4.  **Process (Chain-of-Thought):** Read the document carefully. Filter out irrelevant text. Identify and list the exact data that fulfills the Extraction Goal, ensuring strict adherence to the Formatting Rule."
"\n\n"
"**OUTPUT (Direct Data Only):**"
)

# Initialize Gemini model using the API key from environment
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    # google_api_key=google_api_key
)

# Function definition
def parse_with_gemini(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
        print(f"Parsed batch: {i} of {len(dom_chunks)}")

        
        if hasattr(response, "content"):
            parsed_results.append(response.content)
        else:
            parsed_results.append(str(response))

    return "\n".join(parsed_results)



