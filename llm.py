import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError, ClientError, APIError

# Load .env file for local development
load_dotenv()

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
    return genai.Client(api_key=api_key)

def ask_json(prompt: str, retries: int = 5, delay: int = 10):
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    client = get_client()
    
    # Pause to help avoid free tier rate limits
    time.sleep(2)
    
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            return response.text
        except (ServerError, ClientError, APIError) as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = delay * (attempt + 1)
                print(f"[Rate Limit] Limit reached. Waiting {wait_time}s before retrying... (Attempt {attempt + 1}/{retries})")
                time.sleep(wait_time)
            elif attempt < retries - 1:
                print(f"[Warning] API Error. Retrying in {delay}s... (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)
            else:
                raise e
