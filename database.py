import sqlite3
import os
import hashlib
import datetime
from typing import List, Dict, Tuple, Optional, Any


class Database:
    """
    Database class to handle all SQLite operations for the Moody application.
    """
    def __init__(self, db_name: str = "moody.db"):
        """
        Initialize the database connection and create tables if they don't exist.
        
        Args:
            db_name: The name of the database file
        """
        self.db_name = db_name
        # Configuration pour que chaque thread obtienne sa propre connexion
        self.create_tables()
    
    def get_connection(self):
        """Obtient une connexion à la base de données."""
        # Crée une nouvelle connexion pour chaque opération
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Pour obtenir les résultats sous forme de dictionnaires
        return conn
    
    def close(self, conn) -> None:
        """Ferme la connexion à la base de données."""
        if conn:
            conn.close()
    
    def create_tables(self) -> None:
        """Create all necessary tables for the application if they don't exist."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                gender TEXT NOT NULL,
                last_menstrual_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Mood entries table avec timestamp précis
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                question1_answer INTEGER NOT NULL,
                question2_answer INTEGER NOT NULL,
                question3_answer INTEGER NOT NULL,
                emoji_choice TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')
            
            # Profile information table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                full_name TEXT,
                age INTEGER,
                occupation TEXT,
                interests TEXT,
                goals TEXT,
                additional_notes TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')
            
            conn.commit()
            self.close(conn)
        except sqlite3.Error as e:
            print(f"Table creation error: {e}")
    
    def register_user(self, username: str, email: str, password: str, gender: str, 
                      last_menstrual_date: Optional[str] = None) -> bool:
        """
        Register a new user in the database.
        
        Args:
            username: Username for the new user
            email: Email address for the new user
            password: Password (will be hashed)
            gender: User's gender ('M' or 'F')
            last_menstrual_date: Last menstrual date for female users
            
        Returns:
            Boolean indicating success
        """
        try:
            # Obtenir une connexion
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Hash the password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Insert user data
            cursor.execute('''
            INSERT INTO users (username, email, password_hash, gender, last_menstrual_date) 
            VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, gender, last_menstrual_date))
            
            # Create an empty profile for the user
            user_id = cursor.lastrowid
            cursor.execute('''
            INSERT INTO profile_info (user_id) VALUES (?)
            ''', (user_id,))
            
            conn.commit()
            self.close(conn)
            return True
        except sqlite3.IntegrityError:
            # Username or email already exists
            return False
        except sqlite3.Error as e:
            print(f"Registration error: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user by username and password.
        
        Args:
            username: Username to check
            password: Password to verify
            
        Returns:
            User data dictionary if authenticated, None otherwise
        """
        try:
            # Obtenir une connexion
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Hash the provided password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Check credentials
            cursor.execute('''
            SELECT id, username, email, gender, last_menstrual_date 
            FROM users 
            WHERE username = ? AND password_hash = ?
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            if user:
                user_data = {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "gender": user[3],
                    "last_menstrual_date": user[4]
                }
                self.close(conn)
                return user_data
            self.close(conn)
            return None
        except sqlite3.Error as e:
            print(f"Authentication error: {e}")
            return None
    
    def save_mood_entry(self, user_id: int, question1: int, question2: int, 
                         question3: int, emoji: str, notes: str = '', timestamp: str = None) -> bool:
        """
        Save a mood entry for a user.
        
        Args:
            user_id: ID of the user
            question1: Answer to question 1 (1-3)
            question2: Answer to question 2 (1-3)
            question3: Answer to question 3 (1-3)
            emoji: Selected emoji
            notes: Optional notes
            
        Returns:
            Boolean indicating success
        """
        try:
            # Obtenir une connexion
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Utiliser le timestamp fourni ou l'horodatage actuel
            current_timestamp = timestamp or datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
            INSERT INTO mood_entries (user_id, timestamp, question1_answer, question2_answer, 
                                    question3_answer, emoji_choice, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, current_timestamp, question1, question2, question3, emoji, notes))
            
            conn.commit()
            self.close(conn)
            return True
        except sqlite3.Error as e:
            print(f"Mood entry error: {e}")
            return False
    
    def get_user_mood_entries(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get mood entries for a specific user for the last N days.
        
        Args:
            user_id: ID of the user
            days: Number of days to look back
            
        Returns:
            List of mood entry dictionaries
        """
        try:
            # Obtenir une connexion
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Calculate the date N days ago
            past_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
            
            cursor.execute('''
            SELECT id, timestamp, question1_answer, question2_answer, question3_answer,
                   emoji_choice, notes
            FROM mood_entries
            WHERE user_id = ? AND timestamp >= datetime('now', ?)
            ORDER BY timestamp DESC
            ''', (user_id, f'-{days} days'))
            
            entries = cursor.fetchall()
            result = [
                {
                    "id": entry[0],
                    'date': entry[1],
                    'question1': entry[2],
                    'question2': entry[3],
                    'question3': entry[4],
                    'emoji': entry[5],
                    'notes': entry[6]
                }
                for entry in entries
            ]
            self.close(conn)
            return result
        except sqlite3.Error as e:
            print(f"Get mood entries error: {e}")
            return []
    
    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """
        Get profile information for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Dictionary with profile information
        """
        try:
            # Obtenir une connexion
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT full_name, age, occupation, interests, goals, additional_notes 
            FROM profile_info 
            WHERE user_id = ?
            ''', (user_id,))
            
            profile = cursor.fetchone()
            self.close(conn)
            
            if profile:
                return {
                    "full_name": profile[0] or "",
                    "age": profile[1] or "",
                    "occupation": profile[2] or "",
                    "interests": profile[3] or "",
                    "goals": profile[4] or "",
                    "additional_notes": profile[5] or ""
                }
            return {
                "full_name": "",
                "age": "",
                "occupation": "",
                "interests": "",
                "goals": "",
                "additional_notes": ""
            }
        except sqlite3.Error as e:
            print(f"Get profile error: {e}")
            return {
                "full_name": "",
                "age": "",
                "occupation": "",
                "interests": "",
                "goals": "",
                "additional_notes": ""
            }
    
    def update_user_profile(self, user_id: int, profile_data: Dict[str, Any]) -> bool:
        """
        Update profile information for a user.
        
        Args:
            user_id: ID of the user
            profile_data: Dictionary with profile information
            
        Returns:
            Boolean indicating success
        """
        try:
            # Obtenir une connexion
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            UPDATE profile_info 
            SET full_name = ?, age = ?, occupation = ?, interests = ?, goals = ?, additional_notes = ?, 
                updated_at = CURRENT_TIMESTAMP 
            WHERE user_id = ?
            ''', (
                profile_data.get("full_name", ""),
                profile_data.get("age", ""),
                profile_data.get("occupation", ""),
                profile_data.get("interests", ""),
                profile_data.get("goals", ""),
                profile_data.get("additional_notes", ""),
                user_id
            ))
            
            conn.commit()
            self.close(conn)
            return True
        except sqlite3.Error as e:
            print(f"Update profile error: {e}")
            return False
    
    def update_menstrual_date(self, user_id: int, date: str) -> bool:
        """
        Update the last menstrual date for a female user.
        
        Args:
            user_id: ID of the user
            date: Last menstrual date in YYYY-MM-DD format
            
        Returns:
            Boolean indicating success
        """
        try:
            # Obtenir une connexion
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            UPDATE users 
            SET last_menstrual_date = ? 
            WHERE id = ?
            ''', (date, user_id))
            
            conn.commit()
            self.close(conn)
            return True
        except sqlite3.Error as e:
            print(f"Update menstrual date error: {e}")
            return False
    
    def get_mood_statistics(self, user_id: int) -> Dict[str, Any]:
        """
        Get mood statistics for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            Dictionary with mood statistics
        """
        try:
            # Obtenir une connexion
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get counts of different emoji choices
            cursor.execute('''
            SELECT emoji_choice, COUNT(*) 
            FROM mood_entries 
            WHERE user_id = ? 
            GROUP BY emoji_choice
            ''', (user_id,))
            
            emoji_counts = {emoji: count for emoji, count in cursor.fetchall()}
            
            # Get average answers to questions
            cursor.execute('''
            SELECT 
                AVG(question1_answer) as avg_q1, 
                AVG(question2_answer) as avg_q2, 
                AVG(question3_answer) as avg_q3 
            FROM mood_entries 
            WHERE user_id = ?
            ''', (user_id,))
            
            avgs = cursor.fetchone()
            self.close(conn)
            
            return {
                "emoji_counts": emoji_counts,
                "avg_question1": avgs[0] if avgs and avgs[0] else 0,
                "avg_question2": avgs[1] if avgs and avgs[1] else 0,
                "avg_question3": avgs[2] if avgs and avgs[2] else 0
            }
        except sqlite3.Error as e:
            print(f"Get statistics error: {e}")
            return {
                "emoji_counts": {},
                "avg_question1": 0,
                "avg_question2": 0,
                "avg_question3": 0
            }
