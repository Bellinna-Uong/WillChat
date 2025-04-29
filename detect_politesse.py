def detecter_politesse(texte):
    # Lire le fichier de politesse
    with open('liste/politesse.txt', 'r', encoding='utf-8') as f:
        mots_politesse = [ligne.strip() for ligne in f.readlines()]
    
    for mot in mots_politesse:
        if mot.lower() in texte.lower():
            return "I'm IA not your father, you don't need to be polite..."
    return

# texte = input("Entrez votre texte : ")

# if detecter_politesse(texte):
#     print("Je suis une IA pas ton père, pas besoin d'être poli...")
# else:
#     print("Le texte ne contient pas de mots de politesse.") 