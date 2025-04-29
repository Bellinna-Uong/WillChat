# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
from prompt_config import SYSTEM_PROMPT

# 1) Création de l'app et CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Montage du dossier static sur /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3) Route GET / pour servir index.html
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# 4) Route POST /ask
class AskRequest(BaseModel):
    question: str

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:7b"

@app.post("/ask")
def ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        return {"error": "Question manquante"}

    full_prompt = f"{SYSTEM_PROMPT}\nUser: {question}\nAssistant:"
    payload = {"model": MODEL, "prompt": full_prompt, "stream": False}

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=None)
        resp.raise_for_status()
        result = resp.json()

        answer = result.get("response", "").strip() or "Erreur: réponse vide."
        # Tu peux extraire confidence & link si ton prompt les génère
        confidence = result.get("confidence", "")
        link = result.get("link", "")

        return {
            "response": answer,
            "confidence": confidence,
            "link": link
        }
    except Exception as e:
        print("Ollama call error:", e)
        return {"error": f"Erreur lors de la génération: {e}"}


# Pour lancer le serveur :
# uvicorn main:app --reload --port 8000
# Pour faire une requête :
# curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Hello ??\"}"