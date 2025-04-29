import os
import re

def detecter_manbash(texte):
    # Chemin du fichier contenant les commandes bash
    chemin = os.path.join(os.path.dirname(__file__), '..', 'liste', 'bash.txt')
    
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            cmd_cle = [ligne.strip().lower() for ligne in f if ligne.strip()]
    except FileNotFoundError:
        return "⚠️ Fichier 'bash.txt' non trouvé"

    # Nettoyage et découpage du texte en mots
    mots_texte = re.findall(r'\b\w+\b', texte.lower())  # Extrait les mots (ignore la ponctuation)

    # Détection des mots qui sont des commandes valides
    detected = [mot for mot in mots_texte if mot in cmd_cle]

    # Éviter les doublons
    detected = list(dict.fromkeys(detected))  # Conserve l'ordre sans doublons

    if detected:
        cmds_str = ", ".join(detected)
        return f"We found these commands [: {cmds_str}]. Can you verify if they are commands and list the associated documentation from the man pages?"
    return
