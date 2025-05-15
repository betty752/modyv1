import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime
from database import Database
from utils import center_window

class AuthFrame(ttk.Frame):
    """
    Authentication frame handling login and registration.
    """
    def __init__(self, parent, db: Database, on_auth_success):
        """
        Initialize the authentication frame.
        
        Args:
            parent: Parent widget
            db: Database instance
            on_auth_success: Callback function for successful authentication
        """
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.on_auth_success = on_auth_success
        
        # Create styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 11))
        self.style.configure("TButton", font=("Arial", 11, "bold"))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        
        # Set up the main container
        self.show_login_form()
    
    def show_login_form(self):
        """Display the login form."""
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(padx=40, pady=40, fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.login_frame, text="MOODY", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(self.login_frame, text="Login to Your Account", style="Header.TLabel")
        subtitle_label.pack(pady=(0, 20))
        
        # Username
        username_frame = ttk.Frame(self.login_frame)
        username_frame.pack(fill=tk.X, pady=5)
        
        username_label = ttk.Label(username_frame, text="Username:")
        username_label.pack(anchor=tk.W)
        
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(username_frame, textvariable=self.username_var, width=30)
        username_entry.pack(fill=tk.X, pady=2)
        
        # Password
        password_frame = ttk.Frame(self.login_frame)
        password_frame.pack(fill=tk.X, pady=5)
        
        password_label = ttk.Label(password_frame, text="Password:")
        password_label.pack(anchor=tk.W)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*", width=30)
        password_entry.pack(fill=tk.X, pady=2)
        
        # Login button
        login_button = ttk.Button(self.login_frame, text="Login", command=self.handle_login)
        login_button.pack(pady=20)
        
        # Register link
        register_frame = ttk.Frame(self.login_frame)
        register_frame.pack(pady=10)
        
        register_label = ttk.Label(register_frame, text="Don't have an account?")
        register_label.pack(side=tk.LEFT)
        
        register_link = ttk.Label(register_frame, text="Register", foreground="blue", cursor="hand2")
        register_link.pack(side=tk.LEFT, padx=5)
        register_link.bind("<Button-1>", lambda e: self.show_registration_form())
        
        # Set focus to username
        username_entry.focus_set()
        
        # Pack the main frame
        self.pack(fill=tk.BOTH, expand=True)
    
    def show_registration_form(self):
        """Display the registration form."""
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        self.register_frame = ttk.Frame(self)
        self.register_frame.pack(padx=40, pady=40, fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.register_frame, text="MOODY", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = ttk.Label(self.register_frame, text="Create a New Account", style="Header.TLabel")
        subtitle_label.pack(pady=(0, 20))
        
        # Username
        username_frame = ttk.Frame(self.register_frame)
        username_frame.pack(fill=tk.X, pady=5)
        
        username_label = ttk.Label(username_frame, text="Username:")
        username_label.pack(anchor=tk.W)
        
        self.reg_username_var = tk.StringVar()
        username_entry = ttk.Entry(username_frame, textvariable=self.reg_username_var, width=30)
        username_entry.pack(fill=tk.X, pady=2)
        
        # Email
        email_frame = ttk.Frame(self.register_frame)
        email_frame.pack(fill=tk.X, pady=5)
        
        email_label = ttk.Label(email_frame, text="Email:")
        email_label.pack(anchor=tk.W)
        
        self.reg_email_var = tk.StringVar()
        email_entry = ttk.Entry(email_frame, textvariable=self.reg_email_var, width=30)
        email_entry.pack(fill=tk.X, pady=2)
        
        # Password
        password_frame = ttk.Frame(self.register_frame)
        password_frame.pack(fill=tk.X, pady=5)
        
        password_label = ttk.Label(password_frame, text="Password:")
        password_label.pack(anchor=tk.W)
        
        self.reg_password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.reg_password_var, show="*", width=30)
        password_entry.pack(fill=tk.X, pady=2)
        
        # Confirm Password
        confirm_frame = ttk.Frame(self.register_frame)
        confirm_frame.pack(fill=tk.X, pady=5)
        
        confirm_label = ttk.Label(confirm_frame, text="Confirm Password:")
        confirm_label.pack(anchor=tk.W)
        
        self.reg_confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(confirm_frame, textvariable=self.reg_confirm_var, show="*", width=30)
        confirm_entry.pack(fill=tk.X, pady=2)
        
        # Gender
        gender_frame = ttk.Frame(self.register_frame)
        gender_frame.pack(fill=tk.X, pady=10)
        
        gender_label = ttk.Label(gender_frame, text="Gender:")
        gender_label.pack(anchor=tk.W)
        
        self.gender_var = tk.StringVar(value="M")
        male_radio = ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="M", command=self.toggle_menstrual_field)
        male_radio.pack(side=tk.LEFT, padx=(0, 10))
        
        female_radio = ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="F", command=self.toggle_menstrual_field)
        female_radio.pack(side=tk.LEFT)
        
        # Menstrual cycle date (for female users)
        self.menstrual_frame = ttk.Frame(self.register_frame)
        self.menstrual_frame.pack(fill=tk.X, pady=5)
        self.menstrual_frame.pack_forget()  # Hidden initially
        
        menstrual_label = ttk.Label(self.menstrual_frame, text="Last Menstrual Period Date:")
        menstrual_label.pack(anchor=tk.W)
        
        # Create date entry
        date_frame = ttk.Frame(self.menstrual_frame)
        date_frame.pack(fill=tk.X, pady=2)
        
        self.day_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        
        # Day dropdown
        day_menu = ttk.Combobox(date_frame, textvariable=self.day_var, width=3)
        day_menu['values'] = [str(i).zfill(2) for i in range(1, 32)]
        day_menu.current(0)
        day_menu.pack(side=tk.LEFT, padx=(0, 5))
        
        # Month dropdown
        month_menu = ttk.Combobox(date_frame, textvariable=self.month_var, width=3)
        month_menu['values'] = [str(i).zfill(2) for i in range(1, 13)]
        month_menu.current(0)
        month_menu.pack(side=tk.LEFT, padx=5)
        
        # Year dropdown
        current_year = datetime.now().year
        year_menu = ttk.Combobox(date_frame, textvariable=self.year_var, width=5)
        year_menu['values'] = [str(i) for i in range(current_year-5, current_year+1)]
        year_menu.current(len(year_menu['values'])-1)
        year_menu.pack(side=tk.LEFT, padx=5)
        
        # Register button
        register_button = ttk.Button(self.register_frame, text="Register", command=self.handle_registration)
        register_button.pack(pady=20)
        
        # Login link
        login_frame = ttk.Frame(self.register_frame)
        login_frame.pack(pady=10)
        
        login_label = ttk.Label(login_frame, text="Already have an account?")
        login_label.pack(side=tk.LEFT)
        
        login_link = ttk.Label(login_frame, text="Login", foreground="blue", cursor="hand2")
        login_link.pack(side=tk.LEFT, padx=5)
        login_link.bind("<Button-1>", lambda e: self.show_login_form())
        
        # Set focus to username
        username_entry.focus_set()
        
        # Pack the main frame
        self.pack(fill=tk.BOTH, expand=True)
    
    def toggle_menstrual_field(self):
        """Show or hide the menstrual date field based on gender selection."""
        if self.gender_var.get() == "F":
            self.menstrual_frame.pack(fill=tk.X, pady=5)
        else:
            self.menstrual_frame.pack_forget()
    
    def handle_login(self):
        """Handle the login form submission."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        # Basic validation
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password")
            return
        
        # Attempt to authenticate
        user = self.db.authenticate_user(username, password)
        if user:
            self.on_auth_success(user)
        else:
            messagebox.showerror("Login Error", "Invalid username or password")
    
    def handle_registration(self):
        """Handle the registration form submission."""
        username = self.reg_username_var.get().strip()
        email = self.reg_email_var.get().strip()
        password = self.reg_password_var.get()
        confirm = self.reg_confirm_var.get()
        gender = self.gender_var.get()
        
        # Validate inputs
        if not username or not email or not password or not confirm:
            messagebox.showerror("Registration Error", "All fields are required")
            return
        
        if password != confirm:
            messagebox.showerror("Registration Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Registration Error", "Password must be at least 6 characters")
            return
        
        # Validate email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Registration Error", "Invalid email format")
            return
        
        # Get menstrual date for female users
        menstrual_date = None
        if gender == "F":
            try:
                day = self.day_var.get()
                month = self.month_var.get()
                year = self.year_var.get()
                menstrual_date = f"{year}-{month}-{day}"
                
                # Validate date
                datetime.strptime(menstrual_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Registration Error", "Invalid date format")
                return
        
        # Attempt to register
        success = self.db.register_user(username, email, password, gender, menstrual_date)
        if success:
            messagebox.showinfo("Registration Success", "Account created successfully! You can now login.")
            self.show_login_form()
        else:
            messagebox.showerror("Registration Error", "Username or email already exists")
