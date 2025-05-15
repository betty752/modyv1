"""
SVG Emoji icons for the Moody application.

These are simplified SVG versions of common emojis used in the application
for mood tracking. They are embedded as strings to avoid relying on external image files.
"""

# Very Happy Emoji (😄)
VERY_HAPPY = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="40" height="40">
  <circle cx="50" cy="50" r="45" fill="#FFDD67"/>
  <path d="M69.7,64.8c-5.3,6.6-13.4,10.7-22.1,10.7s-16.9-4.1-22.1-10.7c-1-1.2,0.1-2.8,1.5-2.2c8.8,3.8,14.2,4,20.7,4   s11.9-0.2,20.7-4C70,62,70.7,63.6,69.7,64.8z" fill="#664E27"/>
  <path d="M79.3,32.6c0,4.2-3.4,7.7-7.7,7.7c-4.2,0-7.7-3.4-7.7-7.7c0-4.2,3.4-7.7,7.7-7.7C75.8,24.9,79.3,28.4,79.3,32.6z" fill="#664E27"/>
  <path d="M36,32.6c0,4.2-3.4,7.7-7.7,7.7c-4.2,0-7.7-3.4-7.7-7.7c0-4.2,3.4-7.7,7.7-7.7C32.6,24.9,36,28.4,36,32.6z" fill="#664E27"/>
</svg>
'''

# Happy Emoji (🙂)
HAPPY = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="40" height="40">
  <circle cx="50" cy="50" r="45" fill="#FFDD67"/>
  <path d="M36,45.1c0,4.2-3.4,7.7-7.7,7.7c-4.2,0-7.7-3.4-7.7-7.7" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
  <path d="M79.3,45.1c0,4.2-3.4,7.7-7.7,7.7s-7.7-3.4-7.7-7.7" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
  <path d="M68.2,68.6c-5.3,3.1-11.8,4.9-18.4,4.9s-13-1.8-18.4-4.9" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
</svg>
'''

# Neutral Emoji (😐)
NEUTRAL = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="40" height="40">
  <circle cx="50" cy="50" r="45" fill="#FFDD67"/>
  <circle cx="32.5" cy="38.5" r="5" fill="#664E27"/>
  <circle cx="67.5" cy="38.5" r="5" fill="#664E27"/>
  <path d="M32,68.5h36" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
</svg>
'''

# Sad Emoji (😔)
SAD = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="40" height="40">
  <circle cx="50" cy="50" r="45" fill="#FFDD67"/>
  <circle cx="32.5" cy="38.5" r="5" fill="#664E27"/>
  <circle cx="67.5" cy="38.5" r="5" fill="#664E27"/>
  <path d="M68.2,80c-5.3-3.1-11.8-4.9-18.4-4.9s-13,1.8-18.4,4.9" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
</svg>
'''

# Very Sad Emoji (😢)
VERY_SAD = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="40" height="40">
  <circle cx="50" cy="50" r="45" fill="#FFDD67"/>
  <path d="M36,42.1c0-4.2-3.4-7.7-7.7-7.7c-4.2,0-7.7,3.4-7.7,7.7" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
  <path d="M79.3,42.1c0-4.2-3.4-7.7-7.7-7.7s-7.7,3.4-7.7,7.7" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
  <path d="M68.2,82c-5.3-3.1-11.8-4.9-18.4-4.9s-13,1.8-18.4,4.9" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
  <path d="M65,60c-3,0-3-10-15-10" fill="none" stroke="#65B1EF" stroke-width="5" stroke-linecap="round"/>
  <ellipse cx="71" cy="73" rx="5" ry="6" fill="#65B1EF"/>
</svg>
'''

# Angry Emoji (😡)
ANGRY = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="40" height="40">
  <circle cx="50" cy="50" r="45" fill="#FFDD67"/>
  <path d="M41,38.5c-5.8-4.8-13.7-5-19.7-0.4" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
  <path d="M59,38.5c5.8-4.8,13.7-5,19.7-0.4" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
  <circle cx="32.5" cy="46.5" r="5" fill="#664E27"/>
  <circle cx="67.5" cy="46.5" r="5" fill="#664E27"/>
  <path d="M68.2,75c-5.3-3.1-11.8-4.9-18.4-4.9s-13,1.8-18.4,4.9" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
  <path fill="#E24B4B" d="M50,73.1L50,73.1c-1.9,0-3.5-1.4-3.8-3.3l-1.9-12.6c-0.1-0.9,0.6-1.7,1.5-1.7h8.4c0.9,0,1.6,0.8,1.5,1.7   l-1.9,12.6C53.5,71.7,51.9,73.1,50,73.1z"/>
</svg>
'''

# Tired Emoji (😴)
TIRED = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="40" height="40">
  <circle cx="50" cy="50" r="45" fill="#FFDD67"/>
  <path d="M22,40h18M60,40h18M25,55h50" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
  <path d="M18,28l10,6 M28,28l-10,6" fill="none" stroke="#664E27" stroke-width="3" stroke-linecap="round"/>
  <path d="M82,28l-10,6 M72,28l10,6" fill="none" stroke="#664E27" stroke-width="3" stroke-linecap="round"/>
  <path d="M68.2,75c-5.3-3.1-11.8-4.9-18.4-4.9s-13,1.8-18.4,4.9" fill="none" stroke="#664E27" stroke-width="4" stroke-linecap="round"/>
</svg>
'''

# Anxious Emoji (😰)
ANXIOUS = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="40" height="40">
  <circle cx="50" cy="50" r="45" fill="#FFDD67"/>
  <circle cx="32.5" cy="38.5" r="5" fill="#664E27"/>
  <circle cx="67.5" cy="38.5" r="5" fill="#664E27"/>
  <path d="M44.5,65c0-5.5,11-5.5,11,0" fill="none" stroke="#664E27" stroke-width="3" stroke-linecap="round"/>
  <path d="M85,75c-8.4-0.1-15.8-0.1-20,5" fill="none" stroke="#65B1EF" stroke-width="5" stroke-linecap="round"/>
  <path d="M32,55c0,0,13-4,18,5" fill="none" stroke="#917524" stroke-width="3" stroke-linecap="round"/>
  <path d="M24,50.8C24,48,33,48,33,52" fill="none" stroke="#664E27" stroke-width="3" stroke-linecap="round"/>
  <path d="M68,55c0,0-13-4-18,5" fill="none" stroke="#917524" stroke-width="3" stroke-linecap="round"/>
  <path d="M76,50.8C76,48,67,48,67,52" fill="none" stroke="#664E27" stroke-width="3" stroke-linecap="round"/>
</svg>
'''

# Dictionary to access emojis by name
EMOJIS = {
    "very_happy": VERY_HAPPY,
    "happy": HAPPY,
    "neutral": NEUTRAL,
    "sad": SAD,
    "very_sad": VERY_SAD,
    "angry": ANGRY,
    "tired": TIRED,
    "anxious": ANXIOUS
}

def get_emoji_svg(name):
    """
    Get the SVG string for the specified emoji.
    
    Args:
        name: The name of the emoji
        
    Returns:
        SVG string for the emoji or None if not found
    """
    return EMOJIS.get(name)

def emoji_to_photoimage(name, size=40):
    """
    Convert an emoji SVG to a PhotoImage.
    
    This requires the cairosvg package to be installed.
    If not available, returns None.
    
    Args:
        name: The name of the emoji
        size: Size of the image
        
    Returns:
        PhotoImage or None if conversion failed
    """
    try:
        from tkinter import PhotoImage
        import cairosvg
        import io
        
        svg_data = EMOJIS.get(name)
        if not svg_data:
            return None
        
        png_data = cairosvg.svg2png(bytestring=svg_data.encode(), 
                                     parent_width=size, parent_height=size)
        
        return PhotoImage(data=png_data)
    except ImportError:
        print("cairosvg package not available, cannot convert SVG to PhotoImage")
        return None
    except Exception as e:
        print(f"Error converting emoji to PhotoImage: {e}")
        return None
