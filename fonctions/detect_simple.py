def detect_simple(text):
    text = text.replace("?","").strip()
    text = text.replace(".","")
    text = text.replace(","," ")
    lg = len(text.split(" "))
    if lg < 4:
        return "try in letmegooglethat.com"
    elif lg < 6:
        return "typical, be more specific plz"
    return None

#can you tell me what is the ls and help and cut command make ?