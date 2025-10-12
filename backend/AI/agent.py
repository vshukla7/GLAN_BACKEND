# AI/agent.py
from google.genai import Client
from os import getenv
from dotenv import load_dotenv
import json
import re

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Initialize Gemini client
client = Client(api_key=getenv("GOOGLE_API_KEY"))

# --- Prompt Preamble ---
KNOWLEDGE_BASE = """
You are a helpful assistant that must return only valid JSON.
Do not include markdown, code fences, or explanations.
Do not escape quotes.
Only return raw JSON like this:
{"command": "ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4"}
"""

# --- AI Interaction ---
def ai(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{KNOWLEDGE_BASE}\nUser: {prompt}"
    )
    return response.text.strip()


# --- JSON Cleaner ---
def clean_json(text: str):
    """
    Cleans Gemini output:
    - Removes ```json fences
    - Extracts JSON objects
    - Fixes escaped quotes and sequences
    - Ensures valid Python dict output
    """
    # Remove markdown code fences
    text = re.sub(r"```json|```", "", text).strip()

    # Extract only the JSON-like portion
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        text = match.group(0)

    # Decode escape sequences (e.g., \" -> ")
    text = text.encode("utf-8").decode("unicode_escape")

    # Try parsing as JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to fix double-escaped JSON
        try:
            inner = json.loads(text)
            if isinstance(inner, str):
                return json.loads(inner)
        except Exception:
            pass

    # If still invalid, return fallback for debugging
    return {"error": "Invalid JSON output", "raw": text}


# --- Public interface ---
def Prompt_Taker(prompt: str):
    raw_output = ai(prompt)
    clean_output = clean_json(raw_output)
    return clean_output
