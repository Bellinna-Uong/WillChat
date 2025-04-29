import requests
import random

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:7b"  # Le modèle à utiliser

# Personnalité définie via prompt système
persona = (
    "Tu parle comme un bouffon en info ki fait tro de fautes. Te repond toujour avec des phrases mal ecrites, "
    "genre sms mal taper. Jamai tro serieu, et jamai sans fautes. Tu repond ke en francais."
)

# Fonction pour filtrer les sujets hors informatique
def ifInfo(text):
    try:
        with open("informatique.txt", "r", encoding="utf-8") as f:
            keywords = []
            for line in f:
                line_keywords = [k.strip().lower() for k in line.strip().split(",") if k.strip()]
                keywords.extend(line_keywords)
    except FileNotFoundError:
        return "⚠️ fichier 'informatique.txt' pas trouvé"

    text_lower = text.lower()
    if any(keyword in text_lower for keyword in keywords):
        return None
    else:
        return "Je ne parle que sur des sujets informatique"

def chat_loop():
    print("💬 Assistant spécial prêt. (CTRL+C pour quitter)\n")

    while True:
        user_input = input("Vous: ")

        # Vérifie si la question est hors sujet
        filtre = ifInfo(user_input)
        if filtre:
            print("Bot:", filtre)
            continue

        prompt = persona + f"\nUtilisateur: {user_input}\nAssistant:"
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            })
            data = response.json()
            if "response" in data:
                answer = data["response"].strip()
                print("Bot:", answer)
            else:
                print("❌ Erreur API Ollama:", data)
        except Exception as e:
            print("⚠️ Erreur pendant la requête :", str(e))

if __name__ == "__main__":
    chat_loop()
