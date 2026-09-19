import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError, ClientError, APIError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_json(prompt: str, retries: int = 5, delay: int = 10):
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
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
                time.sleep(wait_time)
            elif attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e
