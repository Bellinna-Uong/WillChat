from fastapi import FastAPI
from pydantic import BaseModel
import requests
from prompt_config import SYSTEM_PROMPT

class AskRequest(BaseModel):
    question: str

app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:7b"

@app.post("/ask")
def ask(req: AskRequest):
    question = req.question.strip()
    print("Received question:", question)
    if not question:
        return {"error": "Question manquante"}

    full_prompt = f"{SYSTEM_PROMPT}\nUser: {question}\nAssistant:"

    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=None)
        print("Ollama status code:", resp.status_code)
        resp.raise_for_status()
        result = resp.json()
        print("Ollama JSON:", result)

        answer = result.get("response", "").strip()
        if not answer:
            answer = "Erreur: réponse vide reçue de la part d'Ollama."

        return {"answer": answer}
    except Exception as e:
        print("ERREUR LORS DE L'APPEL À OLLAMA:", e)
        return {"error": f"Erreur lors de la génération: {e}"}

# Pour lancer le serveur :
# uvicorn main:app --reload --port 8000
# Pour faire une requête :
# curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Hello ??\"}"