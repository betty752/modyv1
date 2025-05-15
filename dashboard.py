import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from database import Database
from utils import center_window, load_themed_image

class DashboardFrame(ttk.Frame):
    """
    Dashboard frame for mood tracking and assessment.
    """
    def __init__(self, parent, db: Database, user_data, navigate_to):
        """
        Initialize the dashboard frame.
        
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
        self.style.configure("Dashboard.TFrame", background="#f0f0f0")
        self.style.configure("Dashboard.TLabel", background="#f0f0f0", font=("Arial", 11))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self.style.configure("Question.TLabel", font=("Arial", 12))
        self.style.configure("ThemeColor.TButton", background=self.theme_color)
        
        self.configure(style="Dashboard.TFrame")
        
        # Question answers
        self.question1_var = tk.IntVar(value=0)
        self.question2_var = tk.IntVar(value=0)
        self.question3_var = tk.IntVar(value=0)
        self.emoji_var = tk.StringVar(value="")
        self.notes_var = tk.StringVar(value="")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all the widgets for the dashboard."""
        # Main container
        main_container = ttk.Frame(self, style="Dashboard.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container, style="Dashboard.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, text="How are you feeling today?", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Navigation buttons
        nav_frame = ttk.Frame(header_frame, style="Dashboard.TFrame")
        nav_frame.pack(side=tk.RIGHT)
        
        profile_btn = ttk.Button(nav_frame, text="Profile", command=lambda: self.navigate_to("profile"))
        profile_btn.pack(side=tk.LEFT, padx=5)
        
        analysis_btn = ttk.Button(nav_frame, text="Analysis", command=lambda: self.navigate_to("analysis"))
        analysis_btn.pack(side=tk.LEFT, padx=5)
        
        suggestions_btn = ttk.Button(nav_frame, text="Suggestions", command=lambda: self.navigate_to("suggestions"))
        suggestions_btn.pack(side=tk.LEFT, padx=5)
        
        # Date display
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        date_label = ttk.Label(main_container, text=current_date, style="Header.TLabel")
        date_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Question 1: Energy level
        q1_frame = ttk.Frame(main_container, style="Dashboard.TFrame")
        q1_frame.pack(fill=tk.X, pady=10)
        
        q1_label = ttk.Label(q1_frame, text="1. How is your energy level today?", style="Question.TLabel")
        q1_label.pack(anchor=tk.W)
        
        q1_options_frame = ttk.Frame(q1_frame, style="Dashboard.TFrame")
        q1_options_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(q1_options_frame, text="Low energy", variable=self.question1_var, value=1).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(q1_options_frame, text="Moderate energy", variable=self.question1_var, value=2).pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(q1_options_frame, text="High energy", variable=self.question1_var, value=3).pack(side=tk.LEFT, padx=15)
        
        # Question 2: Stress level
        q2_frame = ttk.Frame(main_container, style="Dashboard.TFrame")
        q2_frame.pack(fill=tk.X, pady=10)
        
        q2_label = ttk.Label(q2_frame, text="2. How would you rate your stress level?", style="Question.TLabel")
        q2_label.pack(anchor=tk.W)
        
        q2_options_frame = ttk.Frame(q2_frame, style="Dashboard.TFrame")
        q2_options_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(q2_options_frame, text="Low stress", variable=self.question2_var, value=1).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(q2_options_frame, text="Moderate stress", variable=self.question2_var, value=2).pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(q2_options_frame, text="High stress", variable=self.question2_var, value=3).pack(side=tk.LEFT, padx=15)
        
        # Question 3: Overall satisfaction
        q3_frame = ttk.Frame(main_container, style="Dashboard.TFrame")
        q3_frame.pack(fill=tk.X, pady=10)
        
        q3_label = ttk.Label(q3_frame, text="3. How satisfied are you with your day?", style="Question.TLabel")
        q3_label.pack(anchor=tk.W)
        
        q3_options_frame = ttk.Frame(q3_frame, style="Dashboard.TFrame")
        q3_options_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(q3_options_frame, text="Not satisfied", variable=self.question3_var, value=1).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(q3_options_frame, text="Somewhat satisfied", variable=self.question3_var, value=2).pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(q3_options_frame, text="Very satisfied", variable=self.question3_var, value=3).pack(side=tk.LEFT, padx=15)
        
        # Emoji selection
        emoji_frame = ttk.Frame(main_container, style="Dashboard.TFrame")
        emoji_frame.pack(fill=tk.X, pady=20)
        
        emoji_label = ttk.Label(emoji_frame, text="How would you describe your overall mood?", style="Header.TLabel")
        emoji_label.pack(anchor=tk.W, pady=(0, 10))
        
        emoji_selection = ttk.Frame(emoji_frame, style="Dashboard.TFrame")
        emoji_selection.pack(fill=tk.X)
        
        # Emoji buttons
        emojis = [
            ("😄", "very_happy"), 
            ("🙂", "happy"), 
            ("😐", "neutral"), 
            ("😔", "sad"), 
            ("😢", "very_sad"),
            ("😡", "angry"),
            ("😴", "tired"),
            ("😰", "anxious")
        ]
        
        for emoji, value in emojis:
            emoji_btn = ttk.Button(emoji_selection, text=emoji, width=4, command=lambda v=value: self.select_emoji(v))
            emoji_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Selected emoji display
        self.selected_emoji_label = ttk.Label(emoji_frame, text="", style="Title.TLabel")
        self.selected_emoji_label.pack(pady=10)
        
        # Notes section
        notes_frame = ttk.Frame(main_container, style="Dashboard.TFrame")
        notes_frame.pack(fill=tk.X, pady=10)
        
        notes_label = ttk.Label(notes_frame, text="Additional notes:", style="Dashboard.TLabel")
        notes_label.pack(anchor=tk.W)
        
        notes_entry = ttk.Entry(notes_frame, textvariable=self.notes_var, width=50)
        notes_entry.pack(fill=tk.X, pady=5)
        
        # Submit button
        submit_btn = ttk.Button(main_container, text="Save Mood Entry", 
                                command=self.save_mood_entry, style="ThemeColor.TButton")
        submit_btn.pack(pady=20)
        
        # Pack the main frame
        self.pack(fill=tk.BOTH, expand=True)
    
    def select_emoji(self, emoji_value):
        """
        Select an emoji and update the display.
        
        Args:
            emoji_value: The value of the selected emoji
        """
        self.emoji_var.set(emoji_value)
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
        self.selected_emoji_label.configure(text=f"Selected: {emoji_map.get(emoji_value, '')}")
    
    def save_mood_entry(self):
        """Save the mood entry to the database."""
        # Check if all questions answered
        if self.question1_var.get() == 0 or self.question2_var.get() == 0 or self.question3_var.get() == 0:
            messagebox.showerror("Incomplete Entry", "Please answer all three questions.")
            return
        
        # Check if emoji selected
        if not self.emoji_var.get():
            messagebox.showerror("Incomplete Entry", "Please select an emoji to describe your mood.")
            return
        
        # Save to database
        success = self.db.save_mood_entry(
            self.user_data["id"], 
            self.question1_var.get(),
            self.question2_var.get(),
            self.question3_var.get(),
            self.emoji_var.get(),
            self.notes_var.get()
        )
        
        if success:
            messagebox.showinfo("Success", "Your mood entry has been saved successfully!")
            # Navigate to suggestions
            self.navigate_to("suggestions")
        else:
            messagebox.showerror("Error", "There was a problem saving your mood entry. Please try again.")
