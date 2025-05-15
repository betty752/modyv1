import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from database import Database
from auth import AuthFrame
from dashboard import DashboardFrame
from analysis import AnalysisFrame
from suggestions import SuggestionsFrame
from profile import ProfileFrame
from utils import center_window

class MoodyApp:
    """
    Main application class for the Moody mood tracking app.
    """
    def __init__(self, root):
        """
        Initialize the Moody application.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("Moody - Mood Tracking")
        self.root.minsize(800, 600)
        
        # Configure app styles
        self.style = ttk.Style()
        self.setup_styles()
        
        # Initialize database
        self.db = Database()
        
        # Set up variables
        self.current_user = None
        self.current_frame = None
        
        # Create the main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Show the authentication frame
        self.show_auth_frame()
        
        # Center the window
        center_window(self.root, 800, 600)
    
    def setup_styles(self):
        """Set up the application styles."""
        # Configure the application style
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 11))
        self.style.configure("TButton", font=("Arial", 11))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
    
    def show_auth_frame(self):
        """Display the authentication frame."""
        # Clear the current frame if it exists
        if self.current_frame:
            self.current_frame.destroy()
        
        # Create the authentication frame
        self.current_frame = AuthFrame(self.main_container, self.db, self.on_auth_success)
    
    def on_auth_success(self, user_data):
        """
        Handle successful authentication.
        
        Args:
            user_data: Dictionary with user information
        """
        self.current_user = user_data
        self.show_dashboard()
    
    def show_dashboard(self):
        """Display the dashboard frame."""
        # Clear the current frame
        if self.current_frame:
            self.current_frame.destroy()
        
        # Create the dashboard frame
        self.current_frame = DashboardFrame(self.main_container, self.db, self.current_user, self.navigate_to)
    
    def show_analysis(self):
        """Display the analysis frame."""
        # Clear the current frame
        if self.current_frame:
            self.current_frame.destroy()
        
        # Create the analysis frame
        self.current_frame = AnalysisFrame(self.main_container, self.db, self.current_user, self.navigate_to)
    
    def show_suggestions(self):
        """Display the suggestions frame."""
        # Clear the current frame
        if self.current_frame:
            self.current_frame.destroy()
        
        # Create the suggestions frame
        self.current_frame = SuggestionsFrame(self.main_container, self.db, self.current_user, self.navigate_to)
    
    def show_profile(self):
        """Display the profile frame."""
        # Clear the current frame
        if self.current_frame:
            self.current_frame.destroy()
        
        # Create the profile frame
        self.current_frame = ProfileFrame(self.main_container, self.db, self.current_user, self.navigate_to)
    
    def navigate_to(self, page):
        """
        Navigate to a specific page.
        
        Args:
            page: The page to navigate to ("dashboard", "analysis", "suggestions", "profile")
        """
        if page == "dashboard":
            self.show_dashboard()
        elif page == "analysis":
            self.show_analysis()
        elif page == "suggestions":
            self.show_suggestions()
        elif page == "profile":
            self.show_profile()
        else:
            print(f"Unknown page: {page}")

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = MoodyApp(root)
    
    # Handle window close
    def on_closing():
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            # Close the database connection
            app.db.close()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application main loop
    if os.environ.get('REPLIT_HEADLESS'):
        # Running in headless mode (like on Replit)
        print("Application is running headless - server mode")
        # On Replit, just keep the script running
        import time
        while True:
            time.sleep(1)
    else:
        # Start the application main loop
        root.mainloop()

if __name__ == "__main__":
    main()
