import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
from database import Database
from utils import center_window

class AnalysisFrame(ttk.Frame):
    """
    Analysis frame for visualizing mood data.
    """
    def __init__(self, parent, db: Database, user_data, navigate_to):
        """
        Initialize the analysis frame.
        
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
        self.style.configure("Analysis.TFrame", background="#f0f0f0")
        self.style.configure("Analysis.TLabel", background="#f0f0f0", font=("Arial", 11))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self.style.configure("ThemeColor.TButton", background=self.theme_color)
        
        self.configure(style="Analysis.TFrame")
        
        # Period for data visualization
        self.period_var = tk.StringVar(value="30")  # Default to 30 days
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create all the widgets for the analysis page."""
        # Main container
        main_container = ttk.Frame(self, style="Analysis.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container, style="Analysis.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, text="Mood Analysis", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Navigation buttons
        nav_frame = ttk.Frame(header_frame, style="Analysis.TFrame")
        nav_frame.pack(side=tk.RIGHT)
        
        dashboard_btn = ttk.Button(nav_frame, text="Dashboard", command=lambda: self.navigate_to("dashboard"))
        dashboard_btn.pack(side=tk.LEFT, padx=5)
        
        profile_btn = ttk.Button(nav_frame, text="Profile", command=lambda: self.navigate_to("profile"))
        profile_btn.pack(side=tk.LEFT, padx=5)
        
        suggestions_btn = ttk.Button(nav_frame, text="Suggestions", command=lambda: self.navigate_to("suggestions"))
        suggestions_btn.pack(side=tk.LEFT, padx=5)
        
        # Period selection
        period_frame = ttk.Frame(main_container, style="Analysis.TFrame")
        period_frame.pack(fill=tk.X, pady=10)
        
        period_label = ttk.Label(period_frame, text="Select period:", style="Analysis.TLabel")
        period_label.pack(side=tk.LEFT)
        
        ttk.Radiobutton(period_frame, text="7 days", variable=self.period_var, value="7", command=self.load_data).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(period_frame, text="30 days", variable=self.period_var, value="30", command=self.load_data).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(period_frame, text="90 days", variable=self.period_var, value="90", command=self.load_data).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(period_frame, text="All", variable=self.period_var, value="0", command=self.load_data).pack(side=tk.LEFT, padx=10)
        
        # Container for the mood timeline chart
        self.timeline_frame = ttk.Frame(main_container, style="Analysis.TFrame")
        self.timeline_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        timeline_label = ttk.Label(self.timeline_frame, text="Mood Timeline", style="Header.TLabel")
        timeline_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Container for charts and stats
        charts_container = ttk.Frame(main_container, style="Analysis.TFrame")
        charts_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Split into two columns
        left_column = ttk.Frame(charts_container, style="Analysis.TFrame")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_column = ttk.Frame(charts_container, style="Analysis.TFrame")
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Emoji distribution chart container
        self.emoji_frame = ttk.Frame(left_column, style="Analysis.TFrame")
        self.emoji_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        emoji_label = ttk.Label(self.emoji_frame, text="Emotion Distribution", style="Header.TLabel")
        emoji_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Question averages chart container
        self.questions_frame = ttk.Frame(right_column, style="Analysis.TFrame")
        self.questions_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        questions_label = ttk.Label(self.questions_frame, text="Question Averages", style="Header.TLabel")
        questions_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Menstrual cycle correlation for female users
        if self.user_data["gender"] == "F":
            self.cycle_frame = ttk.Frame(main_container, style="Analysis.TFrame")
            self.cycle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            cycle_label = ttk.Label(self.cycle_frame, text="Menstrual Cycle Correlation", style="Header.TLabel")
            cycle_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Pack the main frame
        self.pack(fill=tk.BOTH, expand=True)
    
    def load_data(self):
        """Load and display mood data for analysis."""
        days = int(self.period_var.get())
        entries = self.db.get_user_mood_entries(self.user_data["id"], days if days > 0 else 10000)
        
        if not entries:
            messagebox.showinfo("No Data", "No mood entries found for the selected period.")
            return
        
        # Plot data
        self.plot_timeline(entries)
        self.plot_emoji_distribution(entries)
        self.plot_question_averages(entries)
        
        # Plot menstrual cycle correlation for female users
        if self.user_data["gender"] == "F" and self.user_data["last_menstrual_date"]:
            self.plot_menstrual_correlation(entries)
    
    def plot_timeline(self, entries):
        """
        Plot the mood timeline chart.
        
        Args:
            entries: List of mood entries
        """
        # Clear previous chart if exists
        for widget in self.timeline_frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        
        # Create figure
        fig = Figure(figsize=(10, 3), dpi=100)
        ax = fig.add_subplot(111)
        
        # Prepare data
        dates = [entry["date"] for entry in entries]
        
        # Convert emoji choice to numeric values
        emoji_values = {
            "very_happy": 5,
            "happy": 4,
            "neutral": 3,
            "sad": 2,
            "very_sad": 1,
            "angry": 1.5,
            "tired": 2.5,
            "anxious": 2
        }
        
        values = [emoji_values.get(entry["emoji"], 3) for entry in entries]
        
        # Plot
        ax.plot(dates, values, marker='o', linestyle='-', color=self.theme_color)
        
        # Set y-axis limits and labels
        ax.set_ylim(0.5, 5.5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(["Very Sad", "Sad", "Neutral", "Happy", "Very Happy"])
        
        # Format x-axis
        if len(dates) > 10:
            # Show fewer x labels if there are many dates
            ax.set_xticks([dates[0], dates[len(dates)//2], dates[-1]])
        
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood")
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Adjust layout
        fig.tight_layout()
        
        # Create Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, self.timeline_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def plot_emoji_distribution(self, entries):
        """
        Plot the emoji distribution chart.
        
        Args:
            entries: List of mood entries
        """
        # Clear previous chart if exists
        for widget in self.emoji_frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        
        # Count occurrences of each emoji
        emoji_counts = {}
        for entry in entries:
            emoji = entry["emoji"]
            if emoji in emoji_counts:
                emoji_counts[emoji] += 1
            else:
                emoji_counts[emoji] = 1
        
        # Create mapping for better labels
        emoji_labels = {
            "very_happy": "Very Happy 😄",
            "happy": "Happy 🙂",
            "neutral": "Neutral 😐",
            "sad": "Sad 😔",
            "very_sad": "Very Sad 😢",
            "angry": "Angry 😡",
            "tired": "Tired 😴",
            "anxious": "Anxious 😰"
        }
        
        # Create figure
        fig = Figure(figsize=(4, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Prepare data
        labels = [emoji_labels.get(emoji, emoji) for emoji in emoji_counts.keys()]
        sizes = list(emoji_counts.values())
        colors = [self.theme_color, "#90CAF9", "#A5D6A7", "#FFCC80", "#EF9A9A", "#CE93D8", "#B0BEC5", "#F48FB1"]
        
        # Plot
        ax.pie(sizes, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5))
        
        # Adjust layout
        fig.tight_layout()
        
        # Create Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, self.emoji_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def plot_question_averages(self, entries):
        """
        Plot the question averages chart.
        
        Args:
            entries: List of mood entries
        """
        # Clear previous chart if exists
        for widget in self.questions_frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
        
        # Calculate averages
        q1_sum = sum(entry["question1"] for entry in entries)
        q2_sum = sum(entry["question2"] for entry in entries)
        q3_sum = sum(entry["question3"] for entry in entries)
        
        count = len(entries)
        q1_avg = q1_sum / count
        q2_avg = q2_sum / count
        q3_avg = q3_sum / count
        
        # Create figure
        fig = Figure(figsize=(4, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Prepare data
        questions = ["Energy", "Stress", "Satisfaction"]
        averages = [q1_avg, q2_avg, q3_avg]
        
        # Plot
        bars = ax.bar(questions, averages, color=self.theme_color)
        
        # Add labels
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Set y-axis limits
        ax.set_ylim(0, 3.5)
        ax.set_ylabel("Average Score (1-3)")
        ax.grid(True, linestyle='--', alpha=0.7, axis='y')
        
        # Adjust layout
        fig.tight_layout()
        
        # Create Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, self.questions_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def plot_menstrual_correlation(self, entries):
        """
        Plot the menstrual cycle correlation chart for female users.
        
        Args:
            entries: List of mood entries
        """
        if not self.user_data["last_menstrual_date"]:
            return
            
        # Clear previous chart if exists
        for widget in self.cycle_frame.winfo_children():
            if isinstance(widget, tk.Canvas) or isinstance(widget, ttk.Frame):
                if widget != self.cycle_frame.winfo_children()[0]:  # Keep the title label
                    widget.destroy()
        
        try:
            # Parse the last menstrual date
            last_period = datetime.datetime.strptime(self.user_data["last_menstrual_date"], '%Y-%m-%d').date()
            
            # Create figure
            fig = Figure(figsize=(10, 3), dpi=100)
            ax = fig.add_subplot(111)
            
            # Prepare data
            dates = [datetime.datetime.strptime(entry["date"], '%Y-%m-%d').date() for entry in entries]
            
            # Convert emoji choice to numeric values
            emoji_values = {
                "very_happy": 5,
                "happy": 4,
                "neutral": 3,
                "sad": 2,
                "very_sad": 1,
                "angry": 1.5,
                "tired": 2.5,
                "anxious": 2
            }
            
            values = [emoji_values.get(entry["emoji"], 3) for entry in entries]
            
            # Calculate cycle days
            cycle_days = []
            for date in dates:
                days_since = (date - last_period).days
                cycle_day = days_since % 28 + 1  # Assuming 28-day cycle
                cycle_days.append(cycle_day)
            
            # Plot
            ax.scatter(cycle_days, values, color=self.theme_color, alpha=0.7)
            
            # Add a smooth curve to show trend
            if len(cycle_days) > 3:
                try:
                    import numpy as np
                    from scipy import interpolate
                    
                    # Sort data by cycle day
                    sorted_indices = np.argsort(cycle_days)
                    sorted_cycle_days = [cycle_days[i] for i in sorted_indices]
                    sorted_values = [values[i] for i in sorted_indices]
                    
                    # Create a smooth spline
                    if len(set(sorted_cycle_days)) > 3:  # Need at least 4 unique x values
                        tck = interpolate.splrep(sorted_cycle_days, sorted_values, s=len(sorted_cycle_days))
                        x_new = np.linspace(1, 28, 100)
                        y_new = interpolate.splev(x_new, tck)
                        ax.plot(x_new, y_new, '-', color='#FF69B4', alpha=0.6)
                except (ImportError, ValueError):
                    # If scipy is not available or interpolation fails, use simple line
                    ax.plot(cycle_days, values, '-', color='#FF69B4', alpha=0.4)
            
            # Set axis limits and labels
            ax.set_xlim(1, 28)
            ax.set_ylim(0.5, 5.5)
            ax.set_yticks([1, 2, 3, 4, 5])
            ax.set_yticklabels(["Very Sad", "Sad", "Neutral", "Happy", "Very Happy"])
            
            # Add cycle phase indicators
            ax.axvspan(1, 5, alpha=0.2, color='red', label='Menstruation')
            ax.axvspan(6, 13, alpha=0.2, color='yellow', label='Follicular')
            ax.axvspan(14, 14, alpha=0.2, color='green', label='Ovulation')
            ax.axvspan(15, 28, alpha=0.2, color='blue', label='Luteal')
            
            ax.set_xlabel("Cycle Day")
            ax.set_ylabel("Mood")
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()
            
            # Adjust layout
            fig.tight_layout()
            
            # Create Tkinter canvas
            canvas = FigureCanvasTkAgg(fig, self.cycle_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add explanation
            explanation = (
                "This chart shows your mood patterns throughout your menstrual cycle. "
                "It can help identify if hormonal changes affect your emotions."
            )
            explanation_label = ttk.Label(self.cycle_frame, text=explanation, style="Analysis.TLabel", wraplength=600)
            explanation_label.pack(pady=10)
            
            # Add button to update menstrual date
            update_frame = ttk.Frame(self.cycle_frame, style="Analysis.TFrame")
            update_frame.pack(pady=10)
            
            update_label = ttk.Label(update_frame, text="Update last menstrual period date:", style="Analysis.TLabel")
            update_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Date entry fields
            self.day_var = tk.StringVar(value=last_period.day)
            self.month_var = tk.StringVar(value=last_period.month)
            self.year_var = tk.StringVar(value=last_period.year)
            
            # Day dropdown
            day_menu = ttk.Combobox(update_frame, textvariable=self.day_var, width=3)
            day_menu['values'] = [str(i).zfill(2) for i in range(1, 32)]
            day_menu.pack(side=tk.LEFT, padx=2)
            
            # Month dropdown
            month_menu = ttk.Combobox(update_frame, textvariable=self.month_var, width=3)
            month_menu['values'] = [str(i).zfill(2) for i in range(1, 13)]
            month_menu.pack(side=tk.LEFT, padx=2)
            
            # Year dropdown
            current_year = datetime.datetime.now().year
            year_menu = ttk.Combobox(update_frame, textvariable=self.year_var, width=5)
            year_menu['values'] = [str(i) for i in range(current_year-5, current_year+1)]
            year_menu.pack(side=tk.LEFT, padx=2)
            
            # Update button
            update_btn = ttk.Button(update_frame, text="Update", command=self.update_menstrual_date)
            update_btn.pack(side=tk.LEFT, padx=10)
            
        except (ValueError, TypeError) as e:
            # Display error message if date parsing fails
            error_label = ttk.Label(self.cycle_frame, 
                                     text=f"Could not analyze cycle correlation. Please update your menstrual date in your profile.",
                                     style="Analysis.TLabel")
            error_label.pack(pady=10)
    
    def update_menstrual_date(self):
        """Update the user's last menstrual period date."""
        try:
            day = self.day_var.get()
            month = self.month_var.get()
            year = self.year_var.get()
            new_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            # Validate date
            datetime.datetime.strptime(new_date, '%Y-%m-%d')
            
            # Update in database
            success = self.db.update_menstrual_date(self.user_data["id"], new_date)
            
            if success:
                # Update local user data
                self.user_data["last_menstrual_date"] = new_date
                messagebox.showinfo("Success", "Menstrual period date updated successfully!")
                
                # Refresh the chart
                entries = self.db.get_user_mood_entries(self.user_data["id"], int(self.period_var.get()))
                if entries:
                    self.plot_menstrual_correlation(entries)
            else:
                messagebox.showerror("Error", "Failed to update menstrual period date.")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date.")
