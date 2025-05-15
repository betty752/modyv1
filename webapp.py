"""
Application Moody - Point d'entrée Web

Ce fichier sert de point d'entrée pour l'application web Flask Moody.
Il importe l'application Flask depuis le module web_adapter et la lance
avec les paramètres appropriés.

L'application est configurée pour:
- Être accessible depuis n'importe quelle adresse (0.0.0.0)
- Utiliser le port 5000
- Fonctionner en mode debug pour le développement
"""

from web_adapter.web_app import app

if __name__ == "__main__":
    # Démarrer le serveur Flask
    # host='0.0.0.0' permet d'accéder à l'application depuis l'extérieur
    # debug=True active le rechargement automatique lors des modifications
    app.run(host='0.0.0.0', port=5000, debug=True)