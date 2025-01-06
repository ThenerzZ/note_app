from PySide6.QtGui import QColor

# Color palette
COLORS = {
    'background_dark': '#1a1a1a',
    'background_darker': '#141414',
    'pink_primary': '#ff69b4',
    'pink_light': '#ff8dc7',
    'pink_dark': '#cc5490',
    'text_light': '#ffffff',
    'text_dark': '#e0e0e0',
    'border_light': '#2d2d2d',
    'hover_dark': '#252525'
}

# Main window style
MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {COLORS['background_dark']};
    }}
    QWidget {{
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 10pt;
        color: {COLORS['text_light']};
    }}
"""

# Search bar style
SEARCH_BAR_STYLE = f"""
    QLineEdit {{
        padding: 10px;
        border: 2px solid {COLORS['border_light']};
        border-radius: 8px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        font-size: 11pt;
    }}
    QLineEdit:focus {{
        border: 2px solid {COLORS['pink_primary']};
    }}
"""

# Note list style
NOTE_LIST_STYLE = f"""
    QListWidget {{
        background-color: {COLORS['background_darker']};
        border: none;
        border-radius: 8px;
        padding: 5px;
    }}
    QListWidget::item {{
        background-color: {COLORS['background_darker']};
        border-bottom: 1px solid {COLORS['border_light']};
        padding: 12px;
        border-radius: 4px;
        margin: 2px 5px;
    }}
    QListWidget::item:selected {{
        background-color: {COLORS['pink_dark']};
        color: {COLORS['text_light']};
    }}
    QListWidget::item:hover {{
        background-color: {COLORS['hover_dark']};
    }}
"""

# Button style
BUTTON_STYLE = f"""
    QPushButton {{
        padding: 8px 15px;
        border: none;
        border-radius: 6px;
        background-color: {COLORS['pink_primary']};
        color: {COLORS['text_light']};
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['pink_light']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['pink_dark']};
    }}
"""

# Editor style
EDITOR_STYLE = f"""
    QTextEdit {{
        padding: 15px;
        border: 2px solid {COLORS['border_light']};
        border-radius: 8px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        font-family: 'Consolas', monospace;
        font-size: 11pt;
        line-height: 1.5;
    }}
    QTextEdit:focus {{
        border: 2px solid {COLORS['pink_primary']};
    }}
"""

# Tags input style
TAGS_STYLE = f"""
    QLineEdit {{
        padding: 8px;
        border: 2px solid {COLORS['border_light']};
        border-radius: 6px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        margin-right: 10px;
    }}
    QLineEdit:focus {{
        border: 2px solid {COLORS['pink_primary']};
    }}
    QLabel {{
        color: {COLORS['pink_primary']};
        font-weight: bold;
        margin-right: 5px;
    }}
"""

# Splitter style
SPLITTER_STYLE = f"""
    QSplitter::handle {{
        background-color: {COLORS['border_light']};
        width: 2px;
    }}
    QSplitter::handle:hover {{
        background-color: {COLORS['pink_primary']};
    }}
""" 