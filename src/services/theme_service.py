import json
import os

class ThemeService:
    DEFAULT_THEME = {
        "bg_col": "#E5E7EB",      # Zinc 200
        "fg_col": "#111827",      # Zinc 900
        "surface_col": "#F9FAFB", # Zinc 50
        "border_col": "#FFFFFF",  # White Highlight
        "action_bg": "#0D6EFD",   # Royal Blue
        "action_fg": "white",
        "success_bg": "#198754",  # Forest Green
        "success_fg": "white",
        "warning_bg": "#0DCAF0",  # Bright Cyan
        "warning_fg": "white",
        "danger_bg": "#DC3545",   # Red
        "danger_fg": "white",
        "neutral_bg": "#6C757D",  # Gray
        "neutral_fg": "white",
        "pk_bg": "#FFC107",       # Amber
        "pk_fg": "#111827"        # Dark
    }

    def __init__(self, config_dir="data"):
        self.config_dir = config_dir
        self.theme_path = os.path.join(config_dir, "theme.json")
        self.current_theme = self.load_theme()

    def load_theme(self):
        if os.path.exists(self.theme_path):
            try:
                with open(self.theme_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    # Merge defaults with saved for compatibility
                    theme = self.DEFAULT_THEME.copy()
                    theme.update(saved)
                    return theme
            except Exception:
                return self.DEFAULT_THEME.copy()
        return self.DEFAULT_THEME.copy()

    def save_theme(self, theme_dict=None):
        if theme_dict:
            self.current_theme = theme_dict
        
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
        with open(self.theme_path, "w", encoding="utf-8") as f:
            json.dump(self.current_theme, f, indent=4)

    def get_color(self, key):
        return self.current_theme.get(key, self.DEFAULT_THEME.get(key, "#FF00FF"))
