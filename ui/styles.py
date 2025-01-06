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
    'metadata_text': '#888888',
    'toolbar_bg': '#1f1f1f',
    'separator': '#333333',
    'button_hover': '#2a2a2a',
    'button_pressed': '#1f1f1f',
    'button_checked': '#cc5490'
}

# Main window style
MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {COLORS['background_dark']};
    }}
    QWidget {{
        font-family: 'SF Pro Display', 'Segoe UI', Arial, sans-serif;
        font-size: 10pt;
        color: {COLORS['text_light']};
    }}
    QScrollBar:vertical {{
        border: none;
        background: {COLORS['background_darker']};
        width: 14px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {COLORS['border_light']};
        min-height: 20px;
        border-radius: 7px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {COLORS['pink_dark']};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
        background: none;
    }}
    QScrollBar:horizontal {{
        border: none;
        background: {COLORS['background_darker']};
        height: 14px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background: {COLORS['border_light']};
        min-width: 20px;
        border-radius: 7px;
        margin: 2px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {COLORS['pink_dark']};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
        background: none;
    }}
"""

# Search bar style
SEARCH_BAR_STYLE = f"""
    QLineEdit {{
        padding: 8px 15px;
        border: none;
        border-radius: 8px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        font-size: 11pt;
        margin-bottom: 5px;
    }}
    QLineEdit:focus {{
        background-color: {COLORS['hover_dark']};
        border: 2px solid {COLORS['pink_primary']};
        padding: 6px 13px;
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
        border: none;
        padding: 12px;
        border-radius: 6px;
        margin: 2px 5px;
    }}
    QListWidget::item:selected {{
        background-color: {COLORS['pink_dark']};
        color: {COLORS['text_light']};
    }}
    QListWidget::item:hover:!selected {{
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
        font-weight: 500;
        min-width: 80px;
    }}
    QPushButton:hover {{
        background-color: {COLORS['pink_light']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['pink_dark']};
    }}
"""

# Tool button style
TOOL_BUTTON_STYLE = f"""
    QToolButton {{
        border: none;
        border-radius: 5px;
        background-color: transparent;
        color: {COLORS['text_light']};
        font-weight: 600;
        font-family: 'SF Pro Display', 'Segoe UI', Arial, sans-serif;
        padding: 4px;
        min-width: 32px;
        min-height: 32px;
    }}
    QToolButton:hover {{
        background-color: {COLORS['button_hover']};
    }}
    QToolButton:pressed {{
        background-color: {COLORS['button_pressed']};
    }}
    QToolButton:checked {{
        background-color: {COLORS['button_checked']};
        color: {COLORS['text_light']};
    }}
    QToolButton:disabled {{
        color: {COLORS['metadata_text']};
    }}
"""

# Editor style
EDITOR_STYLE = f"""
    QTextEdit {{
        padding: 20px;
        border: none;
        border-radius: 8px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        font-family: 'SF Pro Text', 'Segoe UI', Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        selection-background-color: {COLORS['pink_dark']};
        selection-color: {COLORS['text_light']};
    }}
    QTextEdit:focus {{
        background-color: {COLORS['hover_dark']};
    }}
"""

# Tags input style
TAGS_STYLE = f"""
    QLineEdit {{
        padding: 8px 15px;
        border: none;
        border-radius: 6px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        margin-right: 10px;
    }}
    QLineEdit:focus {{
        background-color: {COLORS['hover_dark']};
        border: 2px solid {COLORS['pink_primary']};
        padding: 6px 13px;
    }}
    QLabel {{
        color: {COLORS['pink_primary']};
        font-weight: 500;
        margin-right: 5px;
    }}
"""

# Splitter style
SPLITTER_STYLE = f"""
    QSplitter::handle {{
        background-color: {COLORS['border_light']};
        width: 1px;
        margin: 2px;
    }}
    QSplitter::handle:hover {{
        background-color: {COLORS['pink_primary']};
    }}
"""

# Combobox style
COMBOBOX_STYLE = f"""
    QComboBox {{
        padding: 5px 10px;
        border: none;
        border-radius: 6px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        min-width: 60px;
        font-size: 10pt;
    }}
    QComboBox:hover {{
        background-color: {COLORS['hover_dark']};
    }}
    QComboBox:focus {{
        background-color: {COLORS['hover_dark']};
        border: 2px solid {COLORS['pink_primary']};
        padding: 3px 8px;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid {COLORS['text_light']};
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLORS['background_darker']};
        border: 1px solid {COLORS['border_light']};
        border-radius: 6px;
        selection-background-color: {COLORS['pink_dark']};
        selection-color: {COLORS['text_light']};
        padding: 4px;
    }}
    QComboBox QLineEdit {{
        background-color: transparent;
        border: none;
        padding: 0;
        color: {COLORS['text_light']};
        selection-background-color: {COLORS['pink_dark']};
        selection-color: {COLORS['text_light']};
    }}
"""

# Spinbox style
SPINBOX_STYLE = f"""
    QSpinBox {{
        padding: 8px;
        border: none;
        border-radius: 6px;
        background-color: {COLORS['background_darker']};
        color: {COLORS['text_light']};
        min-width: 80px;
    }}
    QSpinBox:hover {{
        background-color: {COLORS['hover_dark']};
    }}
    QSpinBox:focus {{
        background-color: {COLORS['hover_dark']};
        border: 2px solid {COLORS['pink_primary']};
        padding: 6px;
    }}
    QSpinBox::up-button, QSpinBox::down-button {{
        border: none;
        background: transparent;
        width: 16px;
        padding: 0 4px;
    }}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
        background: {COLORS['button_hover']};
    }}
    QSpinBox::up-arrow {{
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-bottom: 4px solid {COLORS['text_light']};
    }}
    QSpinBox::down-arrow {{
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid {COLORS['text_light']};
    }}
"""

# Metadata style
METADATA_STYLE = f"""
    QLabel {{
        color: {COLORS['metadata_text']};
        font-size: 9pt;
        padding: 5px 10px;
        background-color: transparent;
        font-weight: 400;
    }}
"""

# Label style
LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['pink_primary']};
        font-weight: 500;
        font-size: 10pt;
    }}
"""

# Toolbar style
TOOLBAR_STYLE = f"""
    QFrame {{
        background-color: {COLORS['toolbar_bg']};
        border-radius: 8px;
        margin-bottom: 8px;
    }}
"""

# Separator style
SEPARATOR_STYLE = f"""
    QFrame {{
        background-color: {COLORS['separator']};
        width: 1px;
        margin: 4px 8px;
    }}
"""

# Toolbar label style
TOOLBAR_LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_light']};
        font-weight: 500;
        font-size: 10pt;
        margin-right: 2px;
    }}
""" 