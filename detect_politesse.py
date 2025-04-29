def detecter_politesse(texte):
    # Lire le fichier de politesse
    with open('liste/politesse.txt', 'r', encoding='utf-8') as f:
        mots_politesse = [ligne.strip() for ligne in f.readlines()]
    
    # Vérifier si le texte contient un mot de politesse
    for mot in mots_politesse:
        if mot.lower() in texte.lower():
            return True
    return False

# Demander l'input à l'utilisateur
texte = input("Entrez votre texte : ")

# Vérifier et afficher le résultat
if detecter_politesse(texte):
    print("Il ne faut pas être poli !")
else:
    print("Le texte ne contient pas de mots de politesse.") 