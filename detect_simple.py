def detect_simple(text):
    text = text.replace("?","").strip()
    text = text.replace(".","")
    text = text.replace(","," ")
    lg = len(text.split(" "))
    print(lg)
    if lg < 4:
        return "try in letmegooglethat.com"
    elif lg < 6:
        return "typical, be more specific plz"
    return None