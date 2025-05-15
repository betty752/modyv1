import tkinter as tk
from tkinter import ttk
import base64
from io import BytesIO
from PIL import Image, ImageTk

def center_window(window, width=800, height=600):
    """
    Center a tkinter window on the screen.
    
    Args:
        window: The tkinter window
        width: Desired width of the window
        height: Desired height of the window
    """
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position x, y
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set the window size and position
    window.geometry(f"{width}x{height}+{x}+{y}")

def load_themed_image(image_path, width=None, height=None):
    """
    Load an image from a file and optionally resize it.
    
    Args:
        image_path: Path to the image
        width: Optional width to resize to
        height: Optional height to resize to
        
    Returns:
        PhotoImage object that can be used in tkinter widgets
    """
    try:
        image = Image.open(image_path)
        
        # Resize if dimensions are provided
        if width and height:
            image = image.resize((width, height), Image.LANCZOS)
        
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

def create_tooltip(widget, text):
    """
    Create a tooltip for a given widget.
    
    Args:
        widget: The widget to add the tooltip to
        text: The text to display in the tooltip
    """
    def enter(event):
        # Create a toplevel window
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)  # Remove window decorations
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        # Create label
        label = ttk.Label(tooltip, text=text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", "10", "normal"))
        label.pack(ipadx=5, ipady=5)
        
        # Store tooltip reference
        widget.tooltip = tooltip
    
    def leave(event):
        # Destroy tooltip
        if hasattr(widget, "tooltip"):
            widget.tooltip.destroy()
    
    # Bind events
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

def create_rounded_button(parent, text, command, bg_color="#4CAF50", fg_color="white", width=120, height=30):
    """
    Create a button with rounded corners using a Canvas.
    
    Args:
        parent: Parent widget
        text: Button text
        command: Function to call when clicked
        bg_color: Background color
        fg_color: Text color
        width: Button width
        height: Button height
        
    Returns:
        Canvas widget with button functionality
    """
    button = tk.Canvas(parent, width=width, height=height, 
                     bg=parent["background"], bd=0, highlightthickness=0)
    
    # Draw rounded rectangle
    button.create_rectangle(5, 5, width-5, height-5, fill=bg_color, outline=bg_color, width=1,
                          tags=("rect",))
    
    # Create text
    button.create_text(width//2, height//2, text=text, fill=fg_color, font=("Arial", 10, "bold"),
                      tags=("text",))
    
    # Bind events
    def on_click(event):
        command()
    
    def on_enter(event):
        button.itemconfig("rect", fill=adjust_color(bg_color, -20))
    
    def on_leave(event):
        button.itemconfig("rect", fill=bg_color)
    
    button.bind("<Button-1>", on_click)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    
    return button

def adjust_color(hex_color, amount):
    """
    Adjust a hex color by the given amount.
    
    Args:
        hex_color: Hexadecimal color string
        amount: Amount to adjust by (-255 to 255)
        
    Returns:
        Adjusted hexadecimal color string
    """
    # Remove # if present
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    
    # Convert to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Adjust
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    
    # Convert back to hex
    return f"#{r:02x}{g:02x}{b:02x}"

def format_date(date_str):
    """
    Format a date string from YYYY-MM-DD to a more readable format.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Formatted date string
    """
    if not date_str:
        return ""
    
    try:
        import datetime
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return date_str
