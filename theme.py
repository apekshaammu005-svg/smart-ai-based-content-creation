import customtkinter as ctk

# ==========================================
# PROFESSIONAL INDIGO THEME 2026 - PERFECT LIGHT/DARK
# ==========================================

# 🟢 LIGHT MODE - Crisp, modern, enterprise-grade
CLR_LIGHT_BG = "#FFFFFF"          # Pure white background
CLR_LIGHT_SIDEBAR = "#F8FAFC"     # Cool gray sidebar
CLR_LIGHT_ACCENT = "#4F46E5"      # Professional indigo primary
CLR_LIGHT_ACCENT_HOVER = "#3730A3" # Darker indigo hover
CLR_LIGHT_TXT = "#0F172A"         # Deep slate for perfect readability
CLR_LIGHT_TXT_SUB = "#475569"     # Medium slate for secondary text
CLR_LIGHT_BORDER = "#E2E8F0"      # Light border

# 🔴 DARK MODE - Sleek, modern, high contrast
CLR_DARK_BG = "#0A0E1A"           # Deep navy background
CLR_DARK_SIDEBAR = "#111827"      # Charcoal sidebar
CLR_DARK_ACCENT = "#7C3AED"       # Vibrant violet accent
CLR_DARK_ACCENT_HOVER = "#6D28D9" # Deep violet hover
CLR_DARK_TXT = "#F8FAFC"          # Bright white text (perfect contrast)
CLR_DARK_TXT_SUB = "#D1D5DB"      # Light gray secondary
CLR_DARK_BORDER = "#374151"       # Medium gray border

# Legacy (unchanged)
CLR_BG = "#FDFBFF"
CLR_SIDEBAR = "#F0EBFF"
CLR_ACCENT = "#7C3AED"
CLR_ACCENT_HOVER = "#6D28D9"
CLR_TXT = "#1E1B4B"
CLR_BORDER = "#DDD6FE"

def get_theme_color(part):
    """
    Professional theme getter - perfect contrast in ALL modes.
    """
    if ctk.get_appearance_mode() == "Dark":
        colors = {
            "bg": CLR_DARK_BG,
            "sidebar": CLR_DARK_SIDEBAR,
            "accent": CLR_DARK_ACCENT,
            "accent_hover": CLR_DARK_ACCENT_HOVER,
            "txt": CLR_DARK_TXT,
            "txt_sub": CLR_DARK_TXT_SUB,
            "border": CLR_DARK_BORDER,
        }
    else:
        colors = {
            "bg": CLR_LIGHT_BG,
            "sidebar": CLR_LIGHT_SIDEBAR,
            "accent": CLR_LIGHT_ACCENT,
            "accent_hover": CLR_LIGHT_ACCENT_HOVER,
            "txt": CLR_LIGHT_TXT,
            "txt_sub": CLR_LIGHT_TXT_SUB,
            "border": CLR_LIGHT_BORDER,
        }
    return colors.get(part, CLR_ACCENT)

def toggle_theme(app):
    """Toggle light/dark with full UI refresh."""
    current = ctk.get_appearance_mode()
    new_mode = "Light" if current == "Dark" else "Dark"
    ctk.set_appearance_mode(new_mode)
    update_all_theme(app)  # Full refresh

def update_sidebar_colors(app):
    """Update sidebar colors safely."""
    if hasattr(app, 'sidebar') and app.sidebar.winfo_exists():
        sidebar_color = get_theme_color("sidebar")
        app.sidebar.configure(fg_color=sidebar_color)

def update_all_theme(app):

    app.configure(fg_color=get_theme_color("bg"))

    if hasattr(app, 'sidebar') and app.sidebar.winfo_exists():
        app.sidebar.configure(fg_color=get_theme_color("sidebar"))

    if hasattr(app, 'view') and app.view.winfo_exists():
        app.view.configure(fg_color=get_theme_color("bg"))

    app.update_idletasks()

# ==========================================
# USAGE IN YOUR MAIN APP (add to ContentIQ_Pro class)
# ==========================================

