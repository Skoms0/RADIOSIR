import os
import sys
import threading

# Ajouter le dossier include/ au path pour les imports
include_path = os.path.join(os.path.dirname(__file__), 'include')
sys.path.append(include_path)

# Importer les classes
from dataProcess import DataProcess
from api_server import SocketAPI

def start_api():
    api = SocketAPI('data.db')
    api.run(port=5005)

def main():
    # Initialisation
    dp = DataProcess()

    # Lire le fichier test.txt et mettre à jour la base
    file_path = os.path.join(os.path.dirname(__file__), 'test.txt')
    dp.checkAndUpdate(file_path)

    # Lancer l'API dans un thread séparé
    api_thread = threading.Thread(target=start_api)
    api_thread.daemon = True
    api_thread.start()

    print("✅ Serveur API lancé sur http://localhost:5005")
    print("📁 Fichier surveillé :", file_path)
    print("🔁 Appuyez sur Entrée pour quitter.")
    input()

if __name__ == '__main__':
    main()
