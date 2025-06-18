"""
Application Moody - Module Web

Ce module implémente l'interface web de l'application Moody en utilisant Flask.
Il sert d'adaptateur entre la logique métier et l'interface utilisateur web.

L'application permet aux utilisateurs de:
- Créer un compte et se connecter
- Enregistrer leur humeur quotidienne
- Visualiser des analyses de leur humeur
- Recevoir des suggestions personnalisées
- Gérer leur profil
"""

import sys
import os
import json
import datetime
import secrets
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session, flash
from io import BytesIO
from PIL import Image

# Ajouter le répertoire parent au chemin pour permettre les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer les modules de l'application Moody
from database import Database

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Génère une clé secrète aléatoire pour les sessions

# Variables globales pour stocker l'état de l'application
user_data = None      # Données de l'utilisateur connecté
current_mood = None   # Humeur actuelle
mood_history = []     # Historique des humeurs
app_messages = []     # Messages système

# Initialisation de la base de données
db = Database()

@app.route('/')
def index():
    """
    Page d'accueil / connexion de l'application.
    Utilise un template simplifié pour éviter les conflits entre Vue.js et Jinja2.
    """
    # Utiliser le template simplifié
    return render_template('simple_index.html')

@app.route('/dashboard')
def dashboard():
    """
    Tableau de bord pour l'enregistrement des humeurs.
    Accessible uniquement aux utilisateurs authentifiés.
    Permet de répondre aux questions d'évaluation et de sélectionner une humeur.
    """
    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        # L'utilisateur n'est pas connecté, rediriger vers la page de connexion
        return redirect(url_for('index'))
    
    # L'utilisateur est connecté, afficher le tableau de bord
    return render_template('dashboard.html')

@app.route('/suggestions')
def suggestions():
    """
    Page de suggestions personnalisées basées sur l'humeur.
    Accessible uniquement aux utilisateurs authentifiés.
    Offre des recommandations adaptées à l'état émotionnel actuel de l'utilisateur.
    """
    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        # L'utilisateur n'est pas connecté, rediriger vers la page de connexion
        return redirect(url_for('index'))
    
    # L'utilisateur est connecté, afficher la page de suggestions
    return render_template('suggestions.html')

@app.route('/analysis')
def analysis():
    """
    Page d'analyse des données d'humeur avec graphiques.
    Accessible uniquement aux utilisateurs authentifiés.
    Affiche des visualisations pour aider l'utilisateur à comprendre ses tendances d'humeur.
    """
    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        # L'utilisateur n'est pas connecté, rediriger vers la page de connexion
        return redirect(url_for('index'))
    
    # L'utilisateur est connecté, afficher la page d'analyse
    return render_template('analysis.html')

@app.route('/profile')
def profile():
    """
    Page de gestion du profil utilisateur.
    Accessible uniquement aux utilisateurs authentifiés.
    Permet de visualiser et modifier les informations personnelles.
    Pour les utilisatrices, inclut la gestion des dates du cycle menstruel.
    """
    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        # L'utilisateur n'est pas connecté, rediriger vers la page de connexion
        return redirect(url_for('index'))
    
    # L'utilisateur est connecté, afficher la page de profil
    return render_template('profile.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """
    Route pour servir les fichiers statiques (CSS, JavaScript, images, etc.).
    Permet de charger les ressources nécessaires au fonctionnement de l'interface utilisateur.
    
    Args:
        path (str): Chemin du fichier statique demandé
        
    Returns:
        Le fichier statique demandé depuis le répertoire 'static'
    """
    return send_from_directory('static', path)

@app.route('/api/register', methods=['POST'])
def register():
    global user_data
    data = request.json
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    gender = data.get('gender')
    menstrual_date = data.get('menstrual_date') if gender == 'F' else None
    
    success = db.register_user(username, email, password, gender, menstrual_date)
    
    if success:
        # Automatically log in after registration
        user = db.authenticate_user(username, password)
        
        # Store user info in session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['gender'] = user['gender']
        
        # Store in global variable for compatibility
        user_data = user
        
        return jsonify({'success': True, 'redirect': '/dashboard'})
    else:
        return jsonify({'success': False, 'message': 'Username or email already exists'})

@app.route('/api/login', methods=['POST'])
def login():
    global user_data
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    
    user = db.authenticate_user(username, password)
    
    if user:
        # Store user info in session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['gender'] = user['gender']
        
        # Store in global variable for compatibility
        user_data = user
        
        return jsonify({'success': True, 'redirect': '/dashboard'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'})

@app.route('/api/save_mood', methods=['POST'])
def save_mood():
    global current_mood
    data = request.json
    
    if not user_data:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    question1 = int(data.get('question1', 0))
    question2 = int(data.get('question2', 0))
    question3 = int(data.get('question3', 0))
    emoji = data.get('emoji', '')
    notes = data.get('notes', '')
    
    # Obtenir l'horodatage précis
    current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    success = db.save_mood_entry(
        user_data['id'],
        question1, 
        question2, 
        question3, 
        emoji, 
        notes,
        timestamp=current_timestamp
    )
    
    if success:
        # Update current mood avec l'horodatage précis
        current_mood = {
            'date': current_timestamp,
            'question1': question1,
            'question2': question2,
            'question3': question3,
            'emoji': emoji,
            'notes': notes
        }
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Failed to save mood entry'})

@app.route('/api/mood_history', methods=['GET'])
def get_mood_history():
    if not user_data:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    days = request.args.get('days', default=30, type=int)
    entries = db.get_user_mood_entries(user_data['id'], days)
    
    return jsonify({
        'success': True, 
        'entries': entries, 
        'user_gender': user_data.get('gender'),
        'last_menstrual_date': user_data.get('last_menstrual_date')
    })

@app.route('/api/get_latest_mood', methods=['GET'])
def get_latest_mood():
    global user_data, current_mood
    
    if not user_data:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    # Get the last mood entry (we'll just get the last 1 day of entries and take the most recent)
    entries = db.get_user_mood_entries(user_data['id'], 1)
    
    if entries and len(entries) > 0:
        # Return the most recent entry
        return jsonify({
            'success': True,
            'mood': entries[0]
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No mood entries found'
        })

@app.route('/api/profile', methods=['GET'])
def get_profile():
    if not user_data:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    profile = db.get_user_profile(user_data['id'])
    
    return jsonify({'success': True, 'profile': profile, 'user': user_data})

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    if not user_data:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    profile_data = {
        'full_name': data.get('full_name', ''),
        'age': data.get('age', ''),
        'occupation': data.get('occupation', ''),
        'interests': data.get('interests', ''),
        'goals': data.get('goals', ''),
        'additional_notes': data.get('additional_notes', '')
    }
    
    success = db.update_user_profile(user_data['id'], profile_data)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Failed to update profile'})

@app.route('/api/update_menstrual_date', methods=['POST'])
def update_menstrual_date():
    if not user_data or user_data['gender'] != 'F':
        return jsonify({'success': False, 'message': 'Not applicable'})
    
    data = request.json
    date = data.get('date', '')
    
    success = db.update_menstrual_date(user_data['id'], date)
    
    if success:
        # Update local user data
        user_data['last_menstrual_date'] = date
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Failed to update date'})

@app.route('/api/mood_statistics', methods=['GET'])
def get_mood_statistics():
    if not user_data:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    stats = db.get_mood_statistics(user_data['id'])
    
    return jsonify({'success': True, 'statistics': stats})

@app.route('/api/logout', methods=['POST'])
def logout():
    global user_data, current_mood
    
    # Clear session data
    session.clear()
    
    # Clear global variables for compatibility
    user_data = None
    current_mood = None
    
    return jsonify({'success': True, 'redirect': '/'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)