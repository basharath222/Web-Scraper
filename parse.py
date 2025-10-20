import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# load the environment variables from .env
load_dotenv()

# Get the key from the environment
google_api_key = os.getenv("GEMINI_API_KEY")

if not google_api_key:
    raise ValueError("!!!Gemini API key not found! Please check your .env file.!!!")

# 🔹 Prompt Template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}.\n"
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response.\n"
    "3. **Empty Response:** If no information matches the description, return an empty string ('').\n"
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize Gemini model using the API key from environment
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key
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



