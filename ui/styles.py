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
    'hover_dark': '#252525',
    'metadata_text': '#888888'
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

# Tool button style (for formatting toolbar)
TOOL_BUTTON_STYLE = f"""
    QPushButton {{
        padding: 5px;
        border: 1px solid {COLORS['border_light']};
        border-radius: 4px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['hover_dark']};
        border-color: {COLORS['pink_primary']};
    }}
    QPushButton:checked {{
        background-color: {COLORS['pink_dark']};
        border-color: {COLORS['pink_primary']};
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

# Combobox style
COMBOBOX_STYLE = f"""
    QComboBox {{
        padding: 8px;
        border: 2px solid {COLORS['border_light']};
        border-radius: 6px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        min-width: 150px;
    }}
    QComboBox:hover {{
        border-color: {COLORS['pink_primary']};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {COLORS['text_light']};
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLORS['background_darker']};
        border: 2px solid {COLORS['border_light']};
        border-radius: 6px;
        selection-background-color: {COLORS['pink_dark']};
        selection-color: {COLORS['text_light']};
    }}
"""

# Spinbox style
SPINBOX_STYLE = f"""
    QSpinBox {{
        padding: 8px;
        border: 2px solid {COLORS['border_light']};
        border-radius: 6px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        min-width: 80px;
    }}
    QSpinBox:hover {{
        border-color: {COLORS['pink_primary']};
    }}
    QSpinBox::up-button, QSpinBox::down-button {{
        border: none;
        background: {COLORS['background_dark']};
        border-radius: 3px;
        margin: 1px;
    }}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
        background: {COLORS['pink_dark']};
    }}
"""

# Metadata style
METADATA_STYLE = f"""
    QLabel {{
        color: {COLORS['metadata_text']};
        font-size: 9pt;
        padding: 5px;
    }}
""" 