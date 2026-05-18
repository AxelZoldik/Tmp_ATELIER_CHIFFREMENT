import os
import sys
from cryptography.fernet import Fernet

# 1. Récupérer la clé depuis les secrets GitHub (variables d'environnement)
key = os.environ.get('FERNET_KEY')

if not key:
    print("Erreur: La variable d'environnement FERNET_KEY n'est pas définie.")
    sys.exit(1)

# 2. Initialiser Fernet avec cette clé
cipher = Fernet(key)

def encrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    encrypted_data = cipher.encrypt(data)
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)
    print(f"✅ Fichier '{input_file}' chiffré avec succès dans '{output_file}'")

def decrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
    print(f"✅ Fichier '{input_file}' déchiffré avec succès dans '{output_file}'")

# 3. Gérer les commandes du terminal (encrypt / decrypt)
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Utilisation: python app/fernet_atelier1.py <encrypt|decrypt> <fichier_source> <fichier_destination>")
        sys.exit(1)

    action = sys.argv[1]
    fichier_in = sys.argv[2]
    fichier_out = sys.argv[3]

    if action == "encrypt":
        encrypt_file(fichier_in, fichier_out)
    elif action == "decrypt":
        decrypt_file(fichier_in, fichier_out)
    else:
        print("Erreur: L'action doit être 'encrypt' ou 'decrypt'.")