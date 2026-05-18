import hashlib
import urllib.request

# Demande du mot de passe à l'utilisateur
password = input("Entrez votre mot de passe à vérifier : ")

# ---------------------------------------------------------
# 1° - Hachage du mot de passe en SHA-1
# ---------------------------------------------------------
# On génère le hash et on le met en majuscules (.upper()) 
# car l'API de PwnedPasswords renvoie les données en majuscules.
sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

# ---------------------------------------------------------
# 2° - Séparer le préfixe (5 premiers) du suffixe (le reste)
# ---------------------------------------------------------
prefix = sha1_password[:5]
suffix = sha1_password[5:]

print(f"Hash SHA-1 complet : {sha1_password}")
print(f"Préfixe envoyé   : {prefix}")
print(f"Suffixe recherché: {suffix}\n")

# ---------------------------------------------------------
# 3° - Envoi du préfixe à l'API
# ---------------------------------------------------------
url = f"https://api.pwnedpasswords.com/range/{prefix}"

try:
    # On interroge l'API avec le préfixe
    with urllib.request.urlopen(url) as response:
        # L'API renvoie du texte brut. On le lit et on le décode.
        api_data = response.read().decode('utf-8')
        
        # ---------------------------------------------------------
        # 4° - Vérifiez si votre suffixe est présent dans la réponse
        # ---------------------------------------------------------
        # La réponse contient plusieurs lignes du type : "SUFFIXE:NOMBRE_DE_FUITES"
        found = False
        
        for line in api_data.splitlines():
            # On sépare le suffixe renvoyé par l'API et le compteur
            returned_suffix, count = line.split(':')
            
            # Si le suffixe de l'API correspond au nôtre, le mot de passe a fuité !
            if returned_suffix == suffix:
                print(f"❌ ATTENTION : Ce mot de passe a été compromis dans {count} fuite(s) de données !")
                found = True
                break # On arrête la recherche, on a trouvé
        
        if not found:
            print("✅ BONNE NOUVELLE : Ce mot de passe n'a pas été trouvé dans la base de données. Il semble sûr.")

except Exception as e:
    print(f"Une erreur de connexion à l'API s'est produite : {e}")