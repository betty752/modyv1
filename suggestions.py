import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import random
from database import Database
from utils import center_window

class SuggestionsFrame(ttk.Frame):
    """
    Suggestions frame for providing recommendations based on mood.
    """
    def __init__(self, parent, db: Database, user_data, navigate_to):
        """
        Initialize the suggestions frame.
        
        Args:
            parent: Parent widget
            db: Database instance
            user_data: Dictionary with user information
            navigate_to: Function to navigate to other pages
        """
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.user_data = user_data
        self.navigate_to = navigate_to
        
        # Set gender-specific theme color
        self.theme_color = "#FFB6C1" if user_data["gender"] == "F" else "#ADD8E6"  # Light pink for female, light blue for male
        
        # Create styles
        self.style = ttk.Style()
        self.style.configure("Suggestions.TFrame", background="#f0f0f0")
        self.style.configure("Suggestions.TLabel", background="#f0f0f0", font=("Arial", 11))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self.style.configure("Quote.TLabel", font=("Arial", 12, "italic"), wraplength=600)
        self.style.configure("Link.TLabel", font=("Arial", 11, "underline"), foreground="blue", cursor="hand2")
        self.style.configure("Card.TFrame", background="#FFFFFF", relief="raised", borderwidth=1)
        self.style.configure("ThemeColor.TButton", background=self.theme_color)
        
        self.configure(style="Suggestions.TFrame")
        
        # Mood data
        self.current_mood = self.get_latest_mood()
        
        self.create_widgets()
    
    def get_latest_mood(self):
        """
        Get the user's latest mood entry.
        
        Returns:
            Dictionary with mood information or None if no entries exist
        """
        entries = self.db.get_user_mood_entries(self.user_data["id"], 1)
        return entries[0] if entries else None
    
    def create_widgets(self):
        """Create all the widgets for the suggestions page."""
        # Main container
        main_container = ttk.Frame(self, style="Suggestions.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container, style="Suggestions.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, text="Personalized Suggestions", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Navigation buttons
        nav_frame = ttk.Frame(header_frame, style="Suggestions.TFrame")
        nav_frame.pack(side=tk.RIGHT)
        
        dashboard_btn = ttk.Button(nav_frame, text="Dashboard", command=lambda: self.navigate_to("dashboard"))
        dashboard_btn.pack(side=tk.LEFT, padx=5)
        
        analysis_btn = ttk.Button(nav_frame, text="Analysis", command=lambda: self.navigate_to("analysis"))
        analysis_btn.pack(side=tk.LEFT, padx=5)
        
        profile_btn = ttk.Button(nav_frame, text="Profile", command=lambda: self.navigate_to("profile"))
        profile_btn.pack(side=tk.LEFT, padx=5)
        
        # Check if we have mood data
        if not self.current_mood:
            no_data_label = ttk.Label(main_container, 
                               text="No mood data available. Please record your mood on the dashboard first.",
                               style="Header.TLabel")
            no_data_label.pack(pady=50)
            return
        
        # Display current mood
        mood_frame = ttk.Frame(main_container, style="Suggestions.TFrame")
        mood_frame.pack(fill=tk.X, pady=10)
        
        emoji_map = {
            "very_happy": "😄 Very Happy",
            "happy": "🙂 Happy",
            "neutral": "😐 Neutral",
            "sad": "😔 Sad",
            "very_sad": "😢 Very Sad",
            "angry": "😡 Angry",
            "tired": "😴 Tired",
            "anxious": "😰 Anxious"
        }
        
        mood_text = f"Based on your current mood: {emoji_map.get(self.current_mood['emoji'], 'Unknown')}"
        mood_label = ttk.Label(mood_frame, text=mood_text, style="Header.TLabel")
        mood_label.pack(anchor=tk.W)
        
        # Create content based on mood
        self.create_mood_suggestions(main_container)
        
        # Pack the main frame
        self.pack(fill=tk.BOTH, expand=True)
    
    def create_mood_suggestions(self, container):
        """
        Create suggestions based on the user's mood.
        
        Args:
            container: Parent container widget
        """
        mood_type = self.current_mood["emoji"]
        
        # Categorize moods
        positive_moods = ["very_happy", "happy"]
        neutral_moods = ["neutral"]
        negative_moods = ["sad", "very_sad", "angry", "tired", "anxious"]
        
        if mood_type in positive_moods:
            self.create_positive_suggestions(container)
        elif mood_type in neutral_moods:
            self.create_neutral_suggestions(container)
        else:
            self.create_negative_suggestions(container)
    
    def create_positive_suggestions(self, container):
        """
        Create suggestions for positive moods.
        
        Args:
            container: Parent container widget
        """
        # Inspirational quote
        quote_frame = ttk.Frame(container, style="Card.TFrame")
        quote_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        quote_header = ttk.Label(quote_frame, text="Inspirational Quote", style="Header.TLabel")
        quote_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        quotes = [
            "Happiness is not something ready-made. It comes from your own actions. - Dalai Lama",
            "The most wasted of all days is one without laughter. - E.E. Cummings",
            "Happiness is when what you think, what you say, and what you do are in harmony. - Mahatma Gandhi",
            "The happiness of your life depends upon the quality of your thoughts. - Marcus Aurelius",
            "Count your age by friends, not years. Count your life by smiles, not tears. - John Lennon"
        ]
        
        selected_quote = random.choice(quotes)
        quote_label = ttk.Label(quote_frame, text=selected_quote, style="Quote.TLabel")
        quote_label.pack(padx=10, pady=5)
        
        # Music recommendations
        music_frame = ttk.Frame(container, style="Card.TFrame")
        music_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        music_header = ttk.Label(music_frame, text="Uplifting Music", style="Header.TLabel")
        music_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        music_suggestions = [
            ("Happy - Pharrell Williams", "https://www.youtube.com/watch?v=ZbZSe6N_BXs"),
            ("Good Feeling - Flo Rida", "https://www.youtube.com/watch?v=3OnnDqH6Wj8"),
            ("Walking on Sunshine - Katrina & The Waves", "https://www.youtube.com/watch?v=iPUmE-tne5U"),
            ("Can't Stop the Feeling - Justin Timberlake", "https://www.youtube.com/watch?v=ru0K8uYEZWw"),
            ("Uptown Funk - Mark Ronson ft. Bruno Mars", "https://www.youtube.com/watch?v=OPf0YbXqDm0")
        ]
        
        for i, (title, url) in enumerate(music_suggestions[:3]):  # Show only 3
            music_link = ttk.Label(music_frame, text=title, style="Link.TLabel")
            music_link.pack(anchor=tk.W, padx=10, pady=2)
            music_link.bind("<Button-1>", lambda e, url=url: webbrowser.open_new(url))
        
        # Activities to maintain positive mood
        activity_frame = ttk.Frame(container, style="Card.TFrame")
        activity_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        activity_header = ttk.Label(activity_frame, text="Activities to Maintain Your Positivity", style="Header.TLabel")
        activity_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        activities = [
            "Share your positive energy with a friend or family member",
            "Journal about what made you happy today",
            "Try a new hobby or activity that interests you",
            "Express gratitude for three things in your life",
            "Plan something exciting for the future"
        ]
        
        for activity in activities:
            activity_label = ttk.Label(activity_frame, text="• " + activity, style="Suggestions.TLabel")
            activity_label.pack(anchor=tk.W, padx=10, pady=2)
        
        # Energizing video
        video_frame = ttk.Frame(container, style="Card.TFrame")
        video_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        video_header = ttk.Label(video_frame, text="Energizing Videos", style="Header.TLabel")
        video_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        videos = [
            ("Quick Morning Yoga - 10 Min", "https://www.youtube.com/watch?v=VaoV1PrYft4"),
            ("10-Minute Dance Workout", "https://www.youtube.com/watch?v=Rw9S2wb0UxI"),
            ("Guided Meditation for Positive Energy", "https://www.youtube.com/watch?v=86m4RC_ADEY")
        ]
        
        for title, url in videos:
            video_link = ttk.Label(video_frame, text=title, style="Link.TLabel")
            video_link.pack(anchor=tk.W, padx=10, pady=2)
            video_link.bind("<Button-1>", lambda e, url=url: webbrowser.open_new(url))
    
    def create_neutral_suggestions(self, container):
        """
        Create suggestions for neutral moods.
        
        Args:
            container: Parent container widget
        """
        # Inspirational quote
        quote_frame = ttk.Frame(container, style="Card.TFrame")
        quote_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        quote_header = ttk.Label(quote_frame, text="Thought-Provoking Quote", style="Header.TLabel")
        quote_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        quotes = [
            "Life isn't about finding yourself. Life is about creating yourself. - George Bernard Shaw",
            "The only way to do great work is to love what you do. - Steve Jobs",
            "The purpose of our lives is to be happy. - Dalai Lama",
            "The journey of a thousand miles begins with one step. - Lao Tzu",
            "Believe you can and you're halfway there. - Theodore Roosevelt"
        ]
        
        selected_quote = random.choice(quotes)
        quote_label = ttk.Label(quote_frame, text=selected_quote, style="Quote.TLabel")
        quote_label.pack(padx=10, pady=5)
        
        # Music recommendations
        music_frame = ttk.Frame(container, style="Card.TFrame")
        music_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        music_header = ttk.Label(music_frame, text="Mood-Lifting Music", style="Header.TLabel")
        music_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        music_suggestions = [
            ("Here Comes the Sun - The Beatles", "https://www.youtube.com/watch?v=KQetemT1sWc"),
            ("Weightless - Marconi Union", "https://www.youtube.com/watch?v=UfcAVejslrU"),
            ("Lovely Day - Bill Withers", "https://www.youtube.com/watch?v=bEeaS6fuUoA"),
            ("Three Little Birds - Bob Marley", "https://www.youtube.com/watch?v=zaGUr6wzyT8"),
            ("Views - Drake", "https://www.youtube.com/watch?v=uxpDa-c-4Mc")
        ]
        
        for i, (title, url) in enumerate(music_suggestions[:3]):  # Show only 3
            music_link = ttk.Label(music_frame, text=title, style="Link.TLabel")
            music_link.pack(anchor=tk.W, padx=10, pady=2)
            music_link.bind("<Button-1>", lambda e, url=url: webbrowser.open_new(url))
        
        # Activities to improve mood
        activity_frame = ttk.Frame(container, style="Card.TFrame")
        activity_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        activity_header = ttk.Label(activity_frame, text="Activities to Boost Your Mood", style="Header.TLabel")
        activity_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        activities = [
            "Take a short walk outside and notice 5 beautiful things",
            "Create a to-do list to organize your thoughts",
            "Try a new recipe or order your favorite food",
            "Call a friend for a quick chat",
            "Practice mindfulness or deep breathing for 5 minutes"
        ]
        
        for activity in activities:
            activity_label = ttk.Label(activity_frame, text="• " + activity, style="Suggestions.TLabel")
            activity_label.pack(anchor=tk.W, padx=10, pady=2)
        
        # Relaxing video
        video_frame = ttk.Frame(container, style="Card.TFrame")
        video_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        video_header = ttk.Label(video_frame, text="Relaxing & Inspiring Videos", style="Header.TLabel")
        video_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        videos = [
            ("5-Minute Meditation for Balance", "https://www.youtube.com/watch?v=inpok4MKVLM"),
            ("Gentle Yoga Stretch", "https://www.youtube.com/watch?v=4pKly2JojMw"),
            ("Nature Sounds for Relaxation", "https://www.youtube.com/watch?v=eKFTSSKCzWA")
        ]
        
        for title, url in videos:
            video_link = ttk.Label(video_frame, text=title, style="Link.TLabel")
            video_link.pack(anchor=tk.W, padx=10, pady=2)
            video_link.bind("<Button-1>", lambda e, url=url: webbrowser.open_new(url))
    
    def create_negative_suggestions(self, container):
        """
        Create suggestions for negative moods.
        
        Args:
            container: Parent container widget
        """
        # Comforting quote
        quote_frame = ttk.Frame(container, style="Card.TFrame")
        quote_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        quote_header = ttk.Label(quote_frame, text="Comforting Quote", style="Header.TLabel")
        quote_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        quotes = [
            "This too shall pass. - Persian Proverb",
            "You are not alone in your struggles. Every flower must grow through dirt. - Laurie Jean Sennott",
            "Rock bottom became the solid foundation on which I rebuilt my life. - J.K. Rowling",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "The darkest hour is just before the dawn. - Thomas Fuller"
        ]
        
        selected_quote = random.choice(quotes)
        quote_label = ttk.Label(quote_frame, text=selected_quote, style="Quote.TLabel")
        quote_label.pack(padx=10, pady=5)
        
        # Calming music recommendations
        music_frame = ttk.Frame(container, style="Card.TFrame")
        music_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        music_header = ttk.Label(music_frame, text="Calming Music", style="Header.TLabel")
        music_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        music_suggestions = [
            ("Weightless - Marconi Union", "https://www.youtube.com/watch?v=UfcAVejslrU"),
            ("Claire de Lune - Debussy", "https://www.youtube.com/watch?v=CvFH_6DNRCY"),
            ("Breathe Me - Sia", "https://www.youtube.com/watch?v=ghPcYqn0p4Y"),
            ("Peaceful Piano Playlist", "https://www.youtube.com/watch?v=2OEL4P1Rz04"),
            ("Ambient Music for Stress Relief", "https://www.youtube.com/watch?v=lFcSrYw-ARY")
        ]
        
        for i, (title, url) in enumerate(music_suggestions[:3]):  # Show only 3
            music_link = ttk.Label(music_frame, text=title, style="Link.TLabel")
            music_link.pack(anchor=tk.W, padx=10, pady=2)
            music_link.bind("<Button-1>", lambda e, url=url: webbrowser.open_new(url))
        
        # Self-care activities
        activity_frame = ttk.Frame(container, style="Card.TFrame")
        activity_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        activity_header = ttk.Label(activity_frame, text="Self-Care Activities", style="Header.TLabel")
        activity_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        activities = [
            "Take a warm bath or shower",
            "Write down your thoughts and feelings in a journal",
            "Go for a gentle walk outside in nature",
            "Practice deep breathing: inhale for 4 counts, hold for 7, exhale for 8",
            "Reach out to a trusted friend or family member"
        ]
        
        for activity in activities:
            activity_label = ttk.Label(activity_frame, text="• " + activity, style="Suggestions.TLabel")
            activity_label.pack(anchor=tk.W, padx=10, pady=2)
        
        # Relaxing videos
        video_frame = ttk.Frame(container, style="Card.TFrame")
        video_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
        
        video_header = ttk.Label(video_frame, text="Relaxing Videos", style="Header.TLabel")
        video_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        mood_type = self.current_mood["emoji"]
        
        # Different videos depending on the specific negative mood
        if mood_type == "sad" or mood_type == "very_sad":
            videos = [
                ("Gentle Yoga for Sadness", "https://www.youtube.com/watch?v=ybBTfXaFXsE"),
                ("15-Minute Meditation for Emotional Healing", "https://www.youtube.com/watch?v=c1Ndym-IsQg"),
                ("Nature Scenes with Calming Music", "https://www.youtube.com/watch?v=BHACKCNDMW8")
            ]
        elif mood_type == "angry":
            videos = [
                ("Quick Anger Release Meditation", "https://www.youtube.com/watch?v=8vkYJf8DOsc"),
                ("Calming Breathing Exercise", "https://www.youtube.com/watch?v=8VwufJrUhic"),
                ("Relaxing Yoga for Stress Relief", "https://www.youtube.com/watch?v=q5nyrD4eM64")
            ]
        elif mood_type == "anxious":
            videos = [
                ("Anxiety Relief Meditation", "https://www.youtube.com/watch?v=O-6f5wQXSu8"),
                ("Progressive Muscle Relaxation", "https://www.youtube.com/watch?v=86HUcX8ZtAk"),
                ("Calming Visualization Exercise", "https://www.youtube.com/watch?v=yr3g0JR8Zvo")
            ]
        else:  # tired
            videos = [
                ("Energizing Morning Yoga", "https://www.youtube.com/watch?v=k-K6JtJVz9U"),
                ("5-Minute Energy Boost", "https://www.youtube.com/watch?v=rvOLKmOfZX0"),
                ("Revitalizing Breathing Techniques", "https://www.youtube.com/watch?v=AKOjdXByjwc")
            ]
        
        for title, url in videos:
            video_link = ttk.Label(video_frame, text=title, style="Link.TLabel")
            video_link.pack(anchor=tk.W, padx=10, pady=2)
            video_link.bind("<Button-1>", lambda e, url=url: webbrowser.open_new(url))
        
        # Add a specific section for female users during their period
        if self.user_data["gender"] == "F" and self.user_data["last_menstrual_date"]:
            try:
                from datetime import datetime
                
                last_period = datetime.strptime(self.user_data["last_menstrual_date"], '%Y-%m-%d').date()
                today = datetime.now().date()
                days_since = (today - last_period).days
                
                # If within first 7 days of cycle, show period-specific suggestions
                if 0 <= days_since % 28 <= 7:
                    period_frame = ttk.Frame(container, style="Card.TFrame")
                    period_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10, ipadx=10)
                    
                    period_header = ttk.Label(period_frame, text="Period Care Tips", style="Header.TLabel")
                    period_header.pack(anchor=tk.W, padx=10, pady=(10, 5))
                    
                    period_tips = [
                        "Stay hydrated with plenty of water",
                        "Apply a heating pad to relieve cramps",
                        "Take gentle exercise like walking or stretching",
                        "Eat foods rich in iron and avoid excessive caffeine",
                        "Give yourself permission to rest when needed"
                    ]
                    
                    for tip in period_tips:
                        tip_label = ttk.Label(period_frame, text="• " + tip, style="Suggestions.TLabel")
                        tip_label.pack(anchor=tk.W, padx=10, pady=2)
            except (ValueError, TypeError):
                # If date parsing fails, skip this section
                pass
