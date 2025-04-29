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

from fonctions.manBash import detecter_manbash
from fonctions.detect_informatique import ifInfo  # Adaptez l'importation si nécessaire
from fonctions.detect_politesse import detecter_politesse

import difflib

# In-memory history of questions and responses
history = {}

# Initialiser l'application FastAPI
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

# URL du service de génération
GENERATE_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:7b"

# Fonction de similarité de chaînes (utilise difflib pour calculer la similarité)
def get_similarity(question1, question2):
    sequence = difflib.SequenceMatcher(None, question1, question2)
    return sequence.ratio()  # Renvoie un score entre 0 et 1

# Classe de la requête
class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        return {"response": "Error: No question provided.", "confidence": "0%", "link": ""}

    # Vérifier si la question contient une phrase détectée par ifInfo
    if ifInfo(question):
        # Si une phrase spécifique est détectée, utilisez la réponse de ifInfo
        info_response = ifInfo(question)
        return {"response": info_response, "confidence": "100%", "link": ""}

    # Vérifier si la question a déjà été posée dans l'historique
    for stored_question, _ in history.items():
        similarity = get_similarity(question, stored_question)
        if similarity >= 0.7:  # Si la similarité est >= 70%
            return {"response": "Look on the top", "confidence": "100%", "link": ""}

    # URL-encode la question pour les liens potentiels
    encoded_q = urllib.parse.quote(question)

    # Construire le prompt : prompt système + question utilisateur
    prompt = SYSTEM_PROMPT.replace("<url_encoded_question>", encoded_q)
    prompt += detecter_manbash(prompt)
    prompt = prompt + f"\nUser: {question}\nAssistant:"

    try:
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
        resp = requests.post(GENERATE_URL, json=payload, timeout=None)
        resp.raise_for_status()
        data = resp.json()

        # Extraire la réponse brute
        content = data.get("response", "").strip()

        # Supprimer les blocs <think>...</think>
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

        # Essayer d'extraire le JSON
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = content[start:end+1]
        else:
            json_str = content

        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            # En cas d'échec, renvoyez le contenu nettoyé
            response_data = {"response": content, "confidence": "0%", "link": ""}
            history[question] = response_data
            return response_data

        # Construire et stocker la réponse structurée
        response_data = {
            "response": result.get("response", ""),
            "confidence": result.get("confidence", ""),
            "link": result.get("link", "")
        }
        history[question] = response_data
        return response_data

    except Exception as e:
        print("Error calling Ollama:", e)
        return {"response": "Error generating response.", "confidence": "0%", "link": ""}
