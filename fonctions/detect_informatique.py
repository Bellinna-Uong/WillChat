def ifInfo(text):
    try:
        with open("liste/informatique.txt", "r", encoding="utf-8") as f:
            keywords = []
            for line in f:
                line_keywords = [k.strip().lower() for k in line.strip().split(",") if k.strip()]
                keywords.extend(line_keywords)
    except FileNotFoundError:
        return "⚠️ fichier 'informatique.txt' pas trouvé"
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in keywords):
        return
    else:
        return "I'm just informatician bro not rh"