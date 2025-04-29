from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import urllib.parse
import re
import json
from prompt_config import SYSTEM_PROMPT

class AskRequest(BaseModel):
    question: str

# Initialize app and CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Serve static front
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Use the generate endpoint
GENERATE_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:7b"

@app.post("/ask")
def ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        return {"response": "Error: No question provided.", "confidence": "0%", "link": ""}

    # URL-encode question for possible links
    encoded_q = urllib.parse.quote(question)

    # Build prompt: system prompt + user question
    prompt = SYSTEM_PROMPT.replace("<url_encoded_question>", encoded_q)
    prompt = prompt + f"\nUser: {question}\nAssistant:"

    try:
        # Call Ollama generate endpoint
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
        resp = requests.post(GENERATE_URL, json=payload, timeout=None)
        resp.raise_for_status()
        data = resp.json()

        # Extract raw response from generate
        content = data.get("response", "").strip()

        # Remove any <think>...</think> blocks
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

        # Debug log
        print("CLEANED CONTENT:", content)

        # Extract JSON substring
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = content[start:end+1]
        else:
            json_str = content

        # Try parsing JSON
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            # Fallback: return entire cleaned content
            return {"response": content, "confidence": "0%", "link": ""}

        # Return structured fields
        return {
            "response": result.get("response", ""),
            "confidence": result.get("confidence", ""),
            "link": result.get("link", "")
        }
    except Exception as e:
        print("Error calling Ollama:", e)
        return {"response": "Error generating response.", "confidence": "0%", "link": ""}