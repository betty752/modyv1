# Moody - Application de Suivi d'Humeur

## Aperçu Général

Moody est une application complète de suivi d'humeur développée avec Python et Flask. L'application aide les utilisateurs à surveiller leur état émotionnel et à recevoir des recommandations personnalisées pour améliorer leur bien-être. Moody propose des fonctionnalités spécifiques au genre, notamment le suivi du cycle menstruel pour les utilisatrices afin d'identifier les corrélations entre les changements hormonaux et les tendances d'humeur.

## Fonctionnalités

### Authentification des Utilisateurs

- **Inscription**: Les utilisateurs peuvent créer des comptes en fournissant des informations de base:
  - Nom d'utilisateur
  - Email
  - Mot de passe
  - Sélection du genre (Homme/Femme)
  - Date des dernières règles (pour les utilisatrices)
  
- **Connexion**: Système d'authentification sécurisé pour les utilisateurs existants

### Tableau de Bord

L'interface principale où les utilisateurs peuvent enregistrer leur humeur quotidienne en:

- Répondant à trois questions clés sur leur:
  1. Niveau d'énergie (Faible/Modéré/Élevé)
  2. Niveau de stress (Faible/Modéré/Élevé)
  3. Satisfaction générale (Non satisfait/Moyennement satisfait/Très satisfait)
  
- Sélectionnant un emoji qui représente le mieux leur état émotionnel actuel:
  - Très Heureux (😄)
  - Heureux (🙂)
  - Neutre (😐)
  - Triste (😔)
  - Très Triste (😢)
  - En colère (😡)
  - Fatigué (😴)
  - Anxieux (😰)
  
- Ajoutant des notes optionnelles sur leur journée

### Analyse

Une section de visualisation de données qui aide les utilisateurs à comprendre les tendances de leur humeur:

- **Chronologie de l'Humeur**: Graphique chronologique montrant l'évolution de l'humeur au fil du temps
- **Distribution des Émotions**: Diagramme circulaire affichant la fréquence des différentes émotions
- **Moyennes des Questions**: Diagramme à barres montrant les réponses moyennes aux trois questions d'évaluation
- **Corrélation avec le Cycle Menstruel** (pour les utilisatrices): Représentation visuelle de la relation entre les phases du cycle et l'humeur

Les utilisateurs peuvent filtrer les données par différentes périodes:
- 7 jours
- 30 jours
- 90 jours
- Toutes les données enregistrées

### Suggestions

Recommandations personnalisées basées sur l'état émotionnel actuel de l'utilisateur:

- **Pour les Humeurs Positives** (Heureux, Très Heureux):
  - Recommandations de musique inspirante
  - Activités pour maintenir la positivité
  - Vidéos énergisantes
  - Citations inspirantes

- **Pour les Humeurs Neutres**:
  - Citations stimulantes
  - Musique pour améliorer l'humeur
  - Activités pour booster l'humeur
  - Vidéos relaxantes et inspirantes

- **Pour les Humeurs Négatives** (Triste, Très Triste, En colère, Fatigué, Anxieux):
  - Citations réconfortantes
  - Recommandations de musique apaisante
  - Activités d'auto-soins
  - Vidéos de relaxation adaptées à des émotions spécifiques
  - Suggestions spécifiques pour les utilisatrices pendant les menstruations

### Profil

Une section où les utilisateurs peuvent gérer leurs informations personnelles:

- Affichage des informations de base du compte (nom d'utilisateur, genre)
- Détails du profil modifiables:
  - Nom complet
  - Âge
  - Profession
  - Intérêts
  - Objectifs
  - Notes supplémentaires
- Gestion des dates du cycle menstruel (pour les utilisatrices)

## Architecture Technique

### Frontend

- **HTML/CSS/JavaScript**: Interface utilisateur web responsive
- **Flask**: Framework web Python pour servir l'application
- **Chart.js**: Bibliothèque JavaScript pour les visualisations de données et graphiques
- **Icons SVG/CSS**: Icônes et emojis stylisés

### Base de Données

- **SQLite**: Base de données relationnelle légère pour la persistance des données
- **Tables**:
  - `users`: Stocke les informations des comptes utilisateurs
  - `mood_entries`: Enregistre toutes les données de suivi d'humeur
  - `profile_info`: Contient les détails du profil utilisateur

### Design

- **Thème Spécifique au Genre**: 
  - Schéma de couleurs rose pour les utilisatrices
  - Schéma de couleurs bleu pour les utilisateurs masculins
- **Interface Moderne**: Design épuré et intuitif
- **Mise en Page Responsive**: S'adapte à différentes tailles d'écran

## Utilisation de l'Application

### Première Configuration

1. Accédez à l'application dans votre navigateur
2. Sélectionnez "Créer un compte" sur l'écran de connexion
3. Remplissez les informations requises
4. Pour les utilisatrices, entrez la date des dernières règles
5. Soumettez pour créer votre compte

### Suivi Quotidien de l'Humeur

1. Connectez-vous à votre compte
2. Sur le Tableau de Bord, répondez aux trois questions d'évaluation de l'humeur
3. Sélectionnez un emoji qui représente le mieux votre humeur générale
4. Ajoutez des notes sur votre journée (facultatif)
5. Cliquez sur "Enregistrer l'humeur" pour sauvegarder votre entrée

### Consultation des Analyses

1. Naviguez vers la page Analyse en utilisant le menu de navigation
2. Sélectionnez votre période préférée (7, 30, 90 jours, ou Tout)
3. Explorez les différents graphiques pour identifier des tendances
4. Les utilisatrices peuvent voir les corrélations avec leur cycle et mettre à jour les dates si nécessaire

### Obtention de Recommandations

1. Après avoir enregistré votre humeur, vous serez automatiquement dirigé vers la page Suggestions
2. Alternativement, naviguez vers Suggestions en utilisant le menu de navigation
3. Explorez les recommandations personnalisées basées sur votre humeur actuelle
4. Cliquez sur les liens de musique ou de vidéo pour les ouvrir dans votre navigateur

### Gestion de Votre Profil

1. Naviguez vers la page Profil en utilisant le menu de navigation
2. Consultez les informations de votre compte
3. Remplissez ou mettez à jour les détails de votre profil
4. Cliquez sur "Mettre à jour le profil" pour enregistrer les modifications

## Schéma de la Base de Données

### Table users
- `id`: INTEGER PRIMARY KEY
- `username`: TEXT UNIQUE NOT NULL
- `email`: TEXT UNIQUE NOT NULL
- `password_hash`: TEXT NOT NULL
- `gender`: TEXT NOT NULL
- `last_menstrual_date`: TEXT
- `created_at`: TIMESTAMP

### Table mood_entries
- `id`: INTEGER PRIMARY KEY
- `user_id`: INTEGER NOT NULL (Clé étrangère vers users.id)
- `date`: TEXT NOT NULL
- `question1_answer`: INTEGER NOT NULL
- `question2_answer`: INTEGER NOT NULL
- `question3_answer`: INTEGER NOT NULL
- `emoji_choice`: TEXT NOT NULL
- `notes`: TEXT
- `created_at`: TIMESTAMP

### Table profile_info
- `id`: INTEGER PRIMARY KEY
- `user_id`: INTEGER UNIQUE NOT NULL (Clé étrangère vers users.id)
- `full_name`: TEXT
- `age`: INTEGER
- `occupation`: TEXT
- `interests`: TEXT
- `goals`: TEXT
- `additional_notes`: TEXT
- `updated_at`: TIMESTAMP

## Fonctionnalités de Sécurité

- **Hachage des Mots de Passe**: Les mots de passe des utilisateurs sont stockés sous forme de hachages SHA-256, pas en texte brut
- **Validation des Entrées**: Les entrées de formulaire sont validées pour prévenir les attaques par injection
- **Base de Données Sécurisée**: Base de données SQLite avec des contraintes et relations appropriées

## Améliorations Futures

Améliorations potentielles pour les versions futures:

1. **Fonctionnalité d'Exportation**: Permettre aux utilisateurs d'exporter leurs données d'humeur
2. **Notifications**: Rappels pour suivre l'humeur quotidiennement
3. **Analyses Avancées**: Reconnaissance de motifs plus sophistiquée
4. **Fonctionnalités Sociales**: Partage optionnel des insights d'humeur avec des contacts de confiance
5. **Intégration d'Applications Externes**: Synchronisation avec d'autres applications de santé et de fitness

## Dépannage

### Problèmes Courants

1. **Problèmes de Connexion**:
   - Vérifiez votre nom d'utilisateur et mot de passe
   - Assurez-vous d'avoir créé un compte

2. **Problèmes d'Affichage des Graphiques**:
   - Confirmez que vous avez enregistré des entrées d'humeur pour la période sélectionnée
   - Vérifiez que votre navigateur supporte JavaScript et Chart.js

3. **Erreurs de Base de Données**:
   - Assurez-vous que l'application a les permissions d'écriture dans le répertoire
   - Vérifiez que le fichier de base de données n'est pas corrompu

### Obtenir de l'Aide

Si vous rencontrez des problèmes non couverts dans cette documentation:

1. Vérifiez la console de développement de votre navigateur pour les messages d'erreur
2. Assurez-vous que le serveur Flask est en cours d'exécution
3. Vérifiez que votre navigateur est à jour et compatible

## Licence

Cette application est fournie telle quelle sans aucune garantie. Tous droits réservés.

## Crédits

- Développée avec Python, Flask, HTML/CSS/JavaScript et SQLite
- Utilise Chart.js pour la visualisation des données
- Conçue pour une expérience utilisateur optimale

---

*Dernière mise à jour: Mai 2025*
