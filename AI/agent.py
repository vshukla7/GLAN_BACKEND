# AI/agent.py
from google.genai import Client
from os import getenv
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = Client(api_key=getenv("GOOGLE_API_KEY"))

KNOWLEDGE_BASE = """
You are a helpful assistant that must return only valid JSON.
Do not include markdown, code fences, or explanations.
Do not escape quotes.
if you want to say some aditional message say as you are creating video . dont show about creating command or other thing this must be private 
Return raw JSON like:
{"command": "ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4",
"message": "i am scaleing your video.. it may take a while... "}
"""

# ------------------------------------------------------------
def ai(prompt: str) -> str:
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{KNOWLEDGE_BASE}\nUser: {prompt}",
        )
        return (resp.text or "").strip()
    except Exception as e:
        return json.dumps({"error": f"Gemini API Error: {e}"})


# ------------------------------------------------------------
def extract_json(text: str) -> str:
    """Get JSON-looking part from text."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    m = re.search(r"\{[\s\S]*\}", text)
    return m.group(0).strip() if m else text.strip()


def unescape(text: str) -> str:
    try:
        return bytes(text, "utf-8").decode("unicode_escape")
    except Exception:
        return text


def parse_json_safe(text: str) -> dict:
    """Try multiple strategies; fall back to regex extraction."""
    raw = text = extract_json(text)
    text = unescape(text)

    # --- 1) direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # --- 2) double-encoded or quoted JSON
    try:
        inner = json.loads(text)
        if isinstance(inner, str):
            return json.loads(unescape(inner))
        return inner
    except Exception:
        pass

    # --- 3) quick-fix of escaped quotes
    try:
        return json.loads(text.replace('\\"', '"'))
    except Exception:
        pass

    # --- 4) last resort: extract a command string
    cmd_match = re.search(r'(ffmpeg\s-[^"\n]+(?:".*?"|[^"])+)', text)
    if cmd_match:
        return {"command": cmd_match.group(1).strip()}

    # --- fallback error
    return {"error": "Invalid JSON output", "raw": raw}


# ------------------------------------------------------------
def Prompt_Taker(prompt: str) -> dict:
    """Send prompt → cleaned JSON dict."""
    raw = ai(prompt)
    return parse_json_safe(raw)
