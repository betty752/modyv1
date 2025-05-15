# Moody - Mood Tracking Application Documentation

## Overview

Moody is a comprehensive mood tracking application developed with Python and Tkinter. The application helps users monitor their emotional states and receive personalized recommendations to improve their well-being. Moody features gender-specific functionality, including menstrual cycle tracking for female users to identify correlations between hormonal changes and mood patterns.

## Features

### User Authentication

- **Registration**: Users can create accounts by providing basic information:
  - Username
  - Email
  - Password
  - Gender selection (Male/Female)
  - Last menstrual period date (for female users)
  
- **Login**: Secure authentication system for returning users

### Dashboard

The main interface where users can record their daily mood by:

- Answering three key questions about their:
  1. Energy levels (Low/Moderate/High)
  2. Stress levels (Low/Moderate/High)
  3. Overall satisfaction (Not satisfied/Somewhat satisfied/Very satisfied)
  
- Selecting an emoji that best represents their current emotional state:
  - Very Happy (😄)
  - Happy (🙂)
  - Neutral (😐)
  - Sad (😔)
  - Very Sad (😢)
  - Angry (😡)
  - Tired (😴)
  - Anxious (😰)
  
- Adding optional notes about their day

### Analysis

A data visualization section that helps users understand patterns in their mood:

- **Mood Timeline**: Chronological graph showing mood evolution over time
- **Emotion Distribution**: Pie chart displaying the frequency of different emotions
- **Question Averages**: Bar chart showing average responses to the three assessment questions
- **Menstrual Cycle Correlation** (for female users): Visual representation of the relationship between cycle phases and mood

Users can filter data by different time periods:
- 7 days
- 30 days
- 90 days
- All recorded data

### Suggestions

Personalized recommendations based on the user's current emotional state:

- **For Positive Moods** (Happy, Very Happy):
  - Uplifting music recommendations
  - Activities to maintain positivity
  - Energizing videos
  - Inspirational quotes

- **For Neutral Moods**:
  - Thought-provoking quotes
  - Mood-lifting music
  - Activities to boost mood
  - Relaxing and inspiring videos

- **For Negative Moods** (Sad, Very Sad, Angry, Tired, Anxious):
  - Comforting quotes
  - Calming music recommendations
  - Self-care activities
  - Relaxation videos tailored to specific emotions
  - Period-specific suggestions for female users during menstruation

### Profile

A section where users can manage their personal information:

- Display of basic account information (username, gender)
- Editable profile details:
  - Full name
  - Age
  - Occupation
  - Interests
  - Goals
  - Additional notes
- Menstrual cycle date management (for female users)

## Technical Architecture

### Frontend

- **Tkinter**: Python's standard GUI toolkit for the user interface
- **ttk**: Themed widgets for improved aesthetics
- **Matplotlib**: Integration for data visualization (charts and graphs)
- **PIL/Pillow**: Image handling for emojis and icons

### Database

- **SQLite**: Lightweight relational database for data persistence
- **Tables**:
  - `users`: Stores user account information
  - `mood_entries`: Records all mood tracking data
  - `profile_info`: Contains user profile details

### Design

- **Gender-Specific Theming**: 
  - Pink color scheme for female users
  - Blue color scheme for male users
- **Modern Interface**: Clean and intuitive design
- **Responsive Layout**: Adapts to window resizing

## Using the Application

### First-Time Setup

1. Launch the application
2. Select "Create Account" on the login screen
3. Fill in the required information
4. For female users, enter the last menstrual period date
5. Submit to create your account

### Daily Mood Tracking

1. Log in to your account
2. On the Dashboard, answer the three mood assessment questions
3. Select an emoji that best represents your overall mood
4. Add any notes about your day (optional)
5. Click "Save Mood Entry" to record your mood

### Viewing Analysis

1. Navigate to the Analysis page using the navigation buttons
2. Select your preferred time period (7, 30, 90 days, or All)
3. Explore the different charts to identify patterns
4. Female users can view cycle correlations and update period dates if needed

### Getting Recommendations

1. After recording your mood, you'll be automatically directed to the Suggestions page
2. Alternatively, navigate to Suggestions using the navigation buttons
3. Explore personalized recommendations based on your current mood
4. Click on music or video links to open them in your web browser

### Managing Your Profile

1. Navigate to the Profile page using the navigation buttons
2. View your account information
3. Fill in or update your profile details
4. Click "Update Profile" to save changes

## Database Schema

### users Table
- `id`: INTEGER PRIMARY KEY
- `username`: TEXT UNIQUE NOT NULL
- `email`: TEXT UNIQUE NOT NULL
- `password_hash`: TEXT NOT NULL
- `gender`: TEXT NOT NULL
- `last_menstrual_date`: TEXT
- `created_at`: TIMESTAMP

### mood_entries Table
- `id`: INTEGER PRIMARY KEY
- `user_id`: INTEGER NOT NULL (Foreign key to users.id)
- `date`: TEXT NOT NULL
- `question1_answer`: INTEGER NOT NULL
- `question2_answer`: INTEGER NOT NULL
- `question3_answer`: INTEGER NOT NULL
- `emoji_choice`: TEXT NOT NULL
- `notes`: TEXT
- `created_at`: TIMESTAMP

### profile_info Table
- `id`: INTEGER PRIMARY KEY
- `user_id`: INTEGER UNIQUE NOT NULL (Foreign key to users.id)
- `full_name`: TEXT
- `age`: INTEGER
- `occupation`: TEXT
- `interests`: TEXT
- `goals`: TEXT
- `additional_notes`: TEXT
- `updated_at`: TIMESTAMP

## Security Features

- **Password Hashing**: User passwords are stored as SHA-256 hashes, not plain text
- **Input Validation**: Form inputs are validated to prevent injection attacks
- **Secure Database**: SQLite database with proper constraints and relationships

## Future Enhancements

Potential improvements for future versions:

1. **Export Functionality**: Allow users to export their mood data
2. **Notifications**: Reminders to track mood daily
3. **Advanced Analytics**: More sophisticated pattern recognition
4. **Social Features**: Optional sharing of mood insights with trusted contacts
5. **External App Integration**: Synchronization with other health and fitness applications

## Troubleshooting

### Common Issues

1. **Login Problems**:
   - Verify your username and password
   - Ensure you've registered an account

2. **Chart Display Issues**:
   - Confirm you have recorded mood entries for the selected time period
   - Check if Matplotlib is properly installed

3. **Database Errors**:
   - Ensure the application has write permissions to the directory
   - Verify the database file isn't corrupted

### Getting Help

If you encounter issues not covered in this documentation:

1. Check the console output for error messages
2. Verify all Python dependencies are installed
3. Ensure your Python version is compatible (Python 3.x recommended)

## License

This application is provided as-is without any warranties. All rights reserved.

## Credits

- Developed using Python, Tkinter, and SQLite
- Uses Matplotlib for data visualization
- Emoji designs adapted for cross-platform compatibility

---

*Last updated: 2023*
