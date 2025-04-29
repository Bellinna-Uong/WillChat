# WillChat

Pour lancer :
uvicorn main:app --reload --port 8000

Pour poser une question :
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{\"question\":\"${question}\"}'