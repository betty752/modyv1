import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from utils import center_window

class ProfileFrame(ttk.Frame):
    """
    Profile frame for managing user information.
    """
    def __init__(self, parent, db: Database, user_data, navigate_to):
        """
        Initialize the profile frame.
        
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
        self.style.configure("Profile.TFrame", background="#f0f0f0")
        self.style.configure("Profile.TLabel", background="#f0f0f0", font=("Arial", 11))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self.style.configure("Info.TLabel", font=("Arial", 12), padding=5)
        self.style.configure("ThemeColor.TButton", background=self.theme_color)
        
        self.configure(style="Profile.TFrame")
        
        # Load user profile data
        self.profile_data = self.db.get_user_profile(user_data["id"])
        
        # Create string variables for form fields
        self.full_name_var = tk.StringVar(value=self.profile_data.get("full_name", ""))
        self.age_var = tk.StringVar(value=self.profile_data.get("age", ""))
        self.occupation_var = tk.StringVar(value=self.profile_data.get("occupation", ""))
        self.interests_var = tk.StringVar(value=self.profile_data.get("interests", ""))
        self.goals_var = tk.StringVar(value=self.profile_data.get("goals", ""))
        self.notes_var = tk.StringVar(value=self.profile_data.get("additional_notes", ""))
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all the widgets for the profile page."""
        # Main container
        main_container = ttk.Frame(self, style="Profile.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container, style="Profile.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, text="My Profile", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Navigation buttons
        nav_frame = ttk.Frame(header_frame, style="Profile.TFrame")
        nav_frame.pack(side=tk.RIGHT)
        
        dashboard_btn = ttk.Button(nav_frame, text="Dashboard", command=lambda: self.navigate_to("dashboard"))
        dashboard_btn.pack(side=tk.LEFT, padx=5)
        
        analysis_btn = ttk.Button(nav_frame, text="Analysis", command=lambda: self.navigate_to("analysis"))
        analysis_btn.pack(side=tk.LEFT, padx=5)
        
        suggestions_btn = ttk.Button(nav_frame, text="Suggestions", command=lambda: self.navigate_to("suggestions"))
        suggestions_btn.pack(side=tk.LEFT, padx=5)
        
        # Basic info
        info_frame = ttk.Frame(main_container, style="Profile.TFrame")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_label = ttk.Label(info_frame, text="Basic Information", style="Header.TLabel")
        info_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Username (read-only)
        username_frame = ttk.Frame(info_frame, style="Profile.TFrame")
        username_frame.pack(fill=tk.X, pady=5)
        
        username_label = ttk.Label(username_frame, text="Username:", style="Profile.TLabel", width=15, anchor=tk.W)
        username_label.pack(side=tk.LEFT)
        
        username_value = ttk.Label(username_frame, text=self.user_data["username"], style="Info.TLabel")
        username_value.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Gender (read-only)
        gender_frame = ttk.Frame(info_frame, style="Profile.TFrame")
        gender_frame.pack(fill=tk.X, pady=5)
        
        gender_label = ttk.Label(gender_frame, text="Gender:", style="Profile.TLabel", width=15, anchor=tk.W)
        gender_label.pack(side=tk.LEFT)
        
        gender_text = "Female" if self.user_data["gender"] == "F" else "Male"
        gender_value = ttk.Label(gender_frame, text=gender_text, style="Info.TLabel")
        gender_value.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Last menstrual date (for female users)
        if self.user_data["gender"] == "F":
            menstrual_frame = ttk.Frame(info_frame, style="Profile.TFrame")
            menstrual_frame.pack(fill=tk.X, pady=5)
            
            menstrual_label = ttk.Label(menstrual_frame, text="Last Period:", style="Profile.TLabel", width=15, anchor=tk.W)
            menstrual_label.pack(side=tk.LEFT)
            
            menstrual_date = self.user_data.get("last_menstrual_date", "Not set")
            menstrual_value = ttk.Label(menstrual_frame, text=menstrual_date, style="Info.TLabel")
            menstrual_value.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Editable profile information
        profile_frame = ttk.Frame(main_container, style="Profile.TFrame")
        profile_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        profile_label = ttk.Label(profile_frame, text="Profile Details", style="Header.TLabel")
        profile_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Full name
        name_frame = ttk.Frame(profile_frame, style="Profile.TFrame")
        name_frame.pack(fill=tk.X, pady=5)
        
        name_label = ttk.Label(name_frame, text="Full Name:", style="Profile.TLabel", width=15, anchor=tk.W)
        name_label.pack(side=tk.LEFT)
        
        name_entry = ttk.Entry(name_frame, textvariable=self.full_name_var, width=40)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Age
        age_frame = ttk.Frame(profile_frame, style="Profile.TFrame")
        age_frame.pack(fill=tk.X, pady=5)
        
        age_label = ttk.Label(age_frame, text="Age:", style="Profile.TLabel", width=15, anchor=tk.W)
        age_label.pack(side=tk.LEFT)
        
        age_entry = ttk.Entry(age_frame, textvariable=self.age_var, width=10)
        age_entry.pack(side=tk.LEFT)
        
        # Occupation
        occupation_frame = ttk.Frame(profile_frame, style="Profile.TFrame")
        occupation_frame.pack(fill=tk.X, pady=5)
        
        occupation_label = ttk.Label(occupation_frame, text="Occupation:", style="Profile.TLabel", width=15, anchor=tk.W)
        occupation_label.pack(side=tk.LEFT)
        
        occupation_entry = ttk.Entry(occupation_frame, textvariable=self.occupation_var, width=40)
        occupation_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Interests
        interests_frame = ttk.Frame(profile_frame, style="Profile.TFrame")
        interests_frame.pack(fill=tk.X, pady=5)
        
        interests_label = ttk.Label(interests_frame, text="Interests:", style="Profile.TLabel", width=15, anchor=tk.W)
        interests_label.pack(side=tk.LEFT)
        
        interests_entry = ttk.Entry(interests_frame, textvariable=self.interests_var, width=40)
        interests_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Goals
        goals_frame = ttk.Frame(profile_frame, style="Profile.TFrame")
        goals_frame.pack(fill=tk.X, pady=5)
        
        goals_label = ttk.Label(goals_frame, text="Goals:", style="Profile.TLabel", width=15, anchor=tk.W)
        goals_label.pack(side=tk.LEFT)
        
        goals_entry = ttk.Entry(goals_frame, textvariable=self.goals_var, width=40)
        goals_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Additional notes
        notes_frame = ttk.Frame(profile_frame, style="Profile.TFrame")
        notes_frame.pack(fill=tk.X, pady=5)
        
        notes_label = ttk.Label(notes_frame, text="Additional Notes:", style="Profile.TLabel", width=15, anchor=tk.W)
        notes_label.pack(anchor=tk.NW)
        
        notes_text = tk.Text(notes_frame, height=5, width=40, wrap=tk.WORD)
        notes_text.pack(fill=tk.BOTH, expand=True, pady=5)
        notes_text.insert(tk.END, self.profile_data.get("additional_notes", ""))
        
        # Store the Text widget reference for getting content when saving
        self.notes_text = notes_text
        
        # Update button
        update_btn = ttk.Button(main_container, text="Update Profile", command=self.save_profile, style="ThemeColor.TButton")
        update_btn.pack(pady=20)
        
        # Pack the main frame
        self.pack(fill=tk.BOTH, expand=True)
    
    def save_profile(self):
        """Save the profile information to the database."""
        # Validate age if provided
        age_str = self.age_var.get().strip()
        if age_str:
            try:
                age = int(age_str)
                if age < 0 or age > 120:
                    messagebox.showerror("Invalid Age", "Please enter a valid age between 0 and 120.")
                    return
            except ValueError:
                messagebox.showerror("Invalid Age", "Age must be a number.")
                return
        
        # Gather data
        profile_data = {
            "full_name": self.full_name_var.get().strip(),
            "age": age_str,
            "occupation": self.occupation_var.get().strip(),
            "interests": self.interests_var.get().strip(),
            "goals": self.goals_var.get().strip(),
            "additional_notes": self.notes_text.get("1.0", tk.END).strip()
        }
        
        # Save to database
        success = self.db.update_user_profile(self.user_data["id"], profile_data)
        
        if success:
            messagebox.showinfo("Success", "Your profile has been updated successfully!")
            # Update local data
            self.profile_data = profile_data
        else:
            messagebox.showerror("Error", "There was a problem updating your profile. Please try again.")
