import sqlite3
import datetime

def migrate_database():
    # Connexion à la base de données
    conn = sqlite3.connect('moody.db')
    cursor = conn.cursor()
    
    try:
        # 1. Renommer l'ancienne table
        cursor.execute('''ALTER TABLE mood_entries RENAME TO mood_entries_old''')
        
        # 2. Créer la nouvelle table avec la structure mise à jour
        cursor.execute('''
        CREATE TABLE mood_entries (
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
        
        # 3. Copier les données de l'ancienne table vers la nouvelle
        cursor.execute('''
        INSERT INTO mood_entries (
            id, user_id, timestamp, question1_answer, question2_answer, 
            question3_answer, emoji_choice, notes
        )
        SELECT 
            id, user_id, 
            datetime(date || ' ' || time(created_at)), 
            question1_answer, question2_answer, 
            question3_answer, emoji_choice, notes
        FROM mood_entries_old
        ''')
        
        # 4. Supprimer l'ancienne table
        cursor.execute('''DROP TABLE mood_entries_old''')
        
        # 5. Valider les changements
        conn.commit()
        print("Migration réussie!")
        
    except Exception as e:
        # En cas d'erreur, annuler les changements
        conn.rollback()
        print(f"Erreur pendant la migration: {e}")
        
    finally:
        # Fermer la connexion
        conn.close()

if __name__ == '__main__':
    migrate_database()
