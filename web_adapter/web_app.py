import tkinter as tk
import sys
import os
import threading
import time
import json
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session, flash
import base64
from io import BytesIO
from PIL import Image, ImageTk
import datetime
import secrets

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Moody app modules
from database import Database
from main import MoodyApp

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Global variables to store the application state
user_data = None
current_mood = None
mood_history = []
app_messages = []

# Initialize database
db = Database()

@app.route('/')
def index():
    # Use the simplified template instead
    return render_template('simple_index.html')

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user_id' not in session:
        # User is not logged in, redirect to login page
        return redirect(url_for('index'))
    
    # User is logged in, render the dashboard
    return render_template('dashboard.html')

@app.route('/static/<path:path>')
def serve_static(path):
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
        user_data = user
        return jsonify({'success': True, 'user': user})
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
    
    success = db.save_mood_entry(user_data['id'], question1, question2, question3, emoji, notes)
    
    if success:
        # Update current mood
        current_mood = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
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
    
    return jsonify({'success': True, 'entries': entries})

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
    user_data = None
    current_mood = None
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)