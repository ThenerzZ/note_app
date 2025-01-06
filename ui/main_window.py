from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QTextEdit, QLineEdit,
                             QSplitter, QLabel)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QFont
from .styles import *

class MainWindow(QMainWindow):
    # Signals for communication with the controller
    note_selected = Signal(int)  # Emits note_id
    note_deleted = Signal(int)   # Emits note_id
    note_saved = Signal(str, str, str)  # Emits content, title, tags
    search_changed = Signal(str)  # Emits search text

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note Typewriter")
        self.setMinimumSize(1200, 700)
        self.setup_ui()

    def setup_ui(self):
        # Apply main window style
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Create splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet(SPLITTER_STYLE)
        
        # Left panel (Navigation)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Search bar with icon
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search notes...")
        self.search_bar.setStyleSheet(SEARCH_BAR_STYLE)
        self.search_bar.textChanged.connect(lambda text: self.search_changed.emit(text))
        
        # Note list
        self.note_list = QListWidget()
        self.note_list.setStyleSheet(NOTE_LIST_STYLE)
        self.note_list.itemClicked.connect(
            lambda item: self.note_selected.emit(item.data(Qt.UserRole))
        )
        
        # Add widgets to left layout
        left_layout.addWidget(self.search_bar)
        left_layout.addWidget(self.note_list)
        
        # Right panel (Editor)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)
        
        # Toolbar buttons
        self.btn_new = QPushButton("✨ New Note")
        self.btn_save = QPushButton("💾 Save")
        self.btn_delete = QPushButton("🗑️ Delete")
        self.btn_toggle_preview = QPushButton("👁️ Preview")
        
        for btn in [self.btn_new, self.btn_save, self.btn_delete, self.btn_toggle_preview]:
            btn.setStyleSheet(BUTTON_STYLE)
            toolbar_layout.addWidget(btn)
        
        # Tags
        tags_widget = QWidget()
        tags_layout = QHBoxLayout(tags_widget)
        tags_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tags_label = QLabel("🏷️ Tags:")
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Add tags (comma-separated)")
        
        tags_widget.setStyleSheet(TAGS_STYLE)
        tags_layout.addWidget(self.tags_label)
        tags_layout.addWidget(self.tags_input)
        
        toolbar_layout.addWidget(tags_widget)
        toolbar_layout.addStretch()
        
        # Text editor
        self.editor = QTextEdit()
        self.editor.setStyleSheet(EDITOR_STYLE)
        
        # Preview widget
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setStyleSheet(EDITOR_STYLE)
        self.preview.hide()
        
        # Add widgets to right layout
        right_layout.addWidget(toolbar)
        right_layout.addWidget(self.editor)
        right_layout.addWidget(self.preview)
        
        # Add panels to splitter
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        
        # Set initial splitter sizes (35% - 65%)
        self.splitter.setSizes([350, 650])
        
        # Add splitter to main layout
        layout.addWidget(self.splitter)
    
    def refresh_note_list(self, notes):
        self.note_list.clear()
        for note in notes:
            item = QListWidgetItem(f"📝 {note.title}")
            item.setData(Qt.UserRole, note.id)
            self.note_list.addItem(item)
    
    def set_note_content(self, title, content, tags):
        self.editor.setText(content)
        self.tags_input.setText(tags or "")
    
    def get_note_content(self):
        return self.editor.toPlainText()
    
    def get_note_tags(self):
        return self.tags_input.text()
    
    def toggle_preview(self, html_content):
        if self.preview.isHidden():
            self.preview.show()
            self.editor.hide()
            self.preview.setHtml(html_content)
        else:
            self.preview.hide()
            self.editor.show() 