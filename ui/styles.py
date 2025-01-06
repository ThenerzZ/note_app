from PySide6.QtGui import QColor

# Color palette
PINK = "#ff69b4"
DARK_BG = "#141414"
DARKER_BG = "#0a0a0a"
LIGHTER_BG = "#1f1f1f"
BORDER = "#2d2d2d"
TEXT = "#ffffff"
MUTED_TEXT = "#888888"

MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {DARK_BG};
        color: {TEXT};
    }}
"""

MENU_STYLE = f"""
    QMenuBar {{
        background-color: {DARKER_BG};
        color: {TEXT};
        border-bottom: 1px solid {BORDER};
        padding: 1px;
    }}
    QMenuBar::item {{
        background-color: transparent;
        padding: 4px 8px;
        border-radius: 4px;
        margin: 1px;
    }}
    QMenuBar::item:selected {{
        background-color: {PINK};
        color: {DARKER_BG};
    }}
    QMenu {{
        background-color: {DARKER_BG};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 4px;
    }}
    QMenu::item {{
        padding: 4px 24px;
        border-radius: 4px;
    }}
    QMenu::item:selected {{
        background-color: {PINK};
        color: {DARKER_BG};
    }}
    QMenu::separator {{
        height: 1px;
        background-color: {BORDER};
        margin: 4px 0px;
    }}
"""

TOOL_BUTTON_STYLE = f"""
    QToolButton {{
        background-color: transparent;
        color: {TEXT};
        border: 1px solid transparent;
        border-radius: 2px;
        padding: 1px;
        font-weight: bold;
        min-width: 20px;
        max-width: 20px;
        min-height: 20px;
        max-height: 20px;
    }}
    QToolButton:hover {{
        background-color: {LIGHTER_BG};
        border: 1px solid {BORDER};
    }}
    QToolButton:pressed {{
        background-color: {BORDER};
    }}
    QToolButton:checked {{
        background-color: {PINK};
        color: {DARKER_BG};
    }}
"""

SPLITTER_STYLE = f"""
    QSplitter::handle {{
        background-color: {BORDER};
        width: 1px;
    }}
"""

NAV_TOOLBAR_STYLE = f"""
    QFrame {{
        background-color: {LIGHTER_BG};
        border-radius: 4px;
        margin: 0px;
        padding: 0px;
    }}
"""

TOOLBAR_STYLE = f"""
    QFrame {{
        background-color: {LIGHTER_BG};
        border-bottom: 1px solid {BORDER};
        margin: 0px;
        padding: 0px;
        max-height: 28px;
    }}
"""

INFO_BAR_STYLE = f"""
    QFrame {{
        background-color: {LIGHTER_BG};
        border-bottom: 1px solid {BORDER};
        padding: 2px;
    }}
"""

SEARCH_BAR_STYLE = f"""
    QLineEdit {{
        background-color: {DARKER_BG};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 4px;
        padding: 6px;
        font-size: 12px;
        min-height: 24px;
    }}
    QLineEdit:focus {{
        border: 1px solid {PINK};
    }}
"""

COMBOBOX_STYLE = f"""
    QComboBox {{
        background-color: {DARKER_BG};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 12px;
        min-height: 24px;
    }}
    QComboBox:hover {{
        border: 1px solid {PINK};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid {TEXT};
        margin-right: 4px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {DARKER_BG};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 4px;
        padding: 4px;
        selection-background-color: {PINK};
        selection-color: {DARKER_BG};
        min-width: 200px;  /* Match the combo box width */
    }}
"""

NOTE_LIST_STYLE = f"""
    QListWidget {{
        background-color: {DARKER_BG};
        color: {TEXT};
        border: none;
        border-radius: 8px;
        padding: 4px;
        font-size: 13px;
    }}
    QListWidget::item {{
        background-color: {LIGHTER_BG};
        border-radius: 6px;
        padding: 8px;
        margin: 2px 4px;
    }}
    QListWidget::item:selected {{
        background-color: {PINK};
        color: {DARKER_BG};
    }}
    QListWidget::item:hover:!selected {{
        background-color: {BORDER};
    }}
"""

TAGS_STYLE = f"""
    QLineEdit {{
        background-color: {DARKER_BG};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 2px;
        padding: 1px 4px;
        font-size: 11px;
        min-height: 20px;
        max-height: 20px;
    }}
    QLineEdit:focus {{
        border: 1px solid {PINK};
    }}
"""

METADATA_STYLE = f"""
    QLabel {{
        color: {MUTED_TEXT};
        font-size: 11px;
        padding: 0px 4px;
    }}
"""

SEPARATOR_STYLE = f"""
    QFrame {{
        background-color: {BORDER};
        width: 1px;
        margin: 2px 4px;
        max-height: 16px;
    }}
""" 