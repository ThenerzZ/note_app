from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QTextEdit, QLineEdit,
                             QSplitter, QLabel, QListWidgetItem, QToolBar,
                             QFontComboBox, QSpinBox, QComboBox)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import (QIcon, QFont, QKeySequence, QTextCharFormat,
                        QColor, QTextCursor, QAction, QFontDatabase)
from .styles import *

class MainWindow(QMainWindow):
    # Signals
    note_selected = Signal(int)
    note_deleted = Signal(int)
    note_saved = Signal(str, str, str)
    search_changed = Signal(str)
    category_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note Typewriter")
        self.setMinimumSize(1200, 700)
        self.setup_ui()
        self.setup_shortcuts()

    def setup_shortcuts(self):
        # Save shortcut
        save_shortcut = QAction("Save", self)
        save_shortcut.setShortcut(QKeySequence.Save)
        save_shortcut.triggered.connect(lambda: self.btn_save.click())
        self.addAction(save_shortcut)

        # New note shortcut
        new_shortcut = QAction("New", self)
        new_shortcut.setShortcut(QKeySequence("Ctrl+N"))
        new_shortcut.triggered.connect(lambda: self.btn_new.click())
        self.addAction(new_shortcut)

        # Search shortcut
        search_shortcut = QAction("Search", self)
        search_shortcut.setShortcut(QKeySequence("Ctrl+F"))
        search_shortcut.triggered.connect(lambda: self.search_bar.setFocus())
        self.addAction(search_shortcut)

        # Toggle preview shortcut
        preview_shortcut = QAction("Preview", self)
        preview_shortcut.setShortcut(QKeySequence("Ctrl+P"))
        preview_shortcut.triggered.connect(lambda: self.btn_toggle_preview.click())
        self.addAction(preview_shortcut)

    def setup_ui(self):
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        
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
        
        # Category selector
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet(COMBOBOX_STYLE)
        self.category_combo.addItems(["All Notes", "Personal", "Work", "Ideas", "Tasks"])
        self.category_combo.currentTextChanged.connect(self.category_changed.emit)
        left_layout.addWidget(self.category_combo)
        
        # Search bar with icon
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search notes...")
        self.search_bar.setStyleSheet(SEARCH_BAR_STYLE)
        self.search_bar.textChanged.connect(lambda text: self.search_changed.emit(text))
        left_layout.addWidget(self.search_bar)
        
        # Note list
        self.note_list = QListWidget()
        self.note_list.setStyleSheet(NOTE_LIST_STYLE)
        self.note_list.itemClicked.connect(
            lambda item: self.note_selected.emit(item.data(Qt.UserRole))
        )
        left_layout.addWidget(self.note_list)
        
        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)
        
        # Main buttons
        self.btn_new = QPushButton("✨ New Note")
        self.btn_save = QPushButton("💾 Save")
        self.btn_delete = QPushButton("🗑️ Delete")
        self.btn_toggle_preview = QPushButton("👁️ Preview")
        self.btn_export = QPushButton("📤 Export")
        
        for btn in [self.btn_new, self.btn_save, self.btn_delete, 
                   self.btn_toggle_preview, self.btn_export]:
            btn.setStyleSheet(BUTTON_STYLE)
            toolbar_layout.addWidget(btn)
        
        # Formatting toolbar
        format_toolbar = QWidget()
        format_layout = QHBoxLayout(format_toolbar)
        format_layout.setContentsMargins(0, 0, 0, 0)
        format_layout.setSpacing(5)
        
        # Font family
        self.font_family = QFontComboBox()
        self.font_family.setStyleSheet(COMBOBOX_STYLE)
        self.font_family.currentFontChanged.connect(self.format_text)
        
        # Font size
        self.font_size = QSpinBox()
        self.font_size.setStyleSheet(SPINBOX_STYLE)
        self.font_size.setRange(8, 72)
        self.font_size.setValue(11)
        self.font_size.valueChanged.connect(self.format_text)
        
        # Format buttons
        self.btn_bold = QPushButton("B")
        self.btn_italic = QPushButton("I")
        self.btn_underline = QPushButton("U")
        self.btn_color = QPushButton("🎨")
        
        for btn in [self.btn_bold, self.btn_italic, self.btn_underline, self.btn_color]:
            btn.setStyleSheet(TOOL_BUTTON_STYLE)
            btn.setFixedSize(30, 30)
            format_layout.addWidget(btn)
        
        format_layout.addWidget(self.font_family)
        format_layout.addWidget(self.font_size)
        format_layout.addStretch()
        
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
        
        # Add all toolbars to right layout
        right_layout.addWidget(toolbar)
        right_layout.addWidget(format_toolbar)
        
        # Editor and metadata
        self.metadata_label = QLabel()
        self.metadata_label.setStyleSheet(METADATA_STYLE)
        right_layout.addWidget(self.metadata_label)
        
        # Text editor
        self.editor = QTextEdit()
        self.editor.setStyleSheet(EDITOR_STYLE)
        
        # Preview widget
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setStyleSheet(EDITOR_STYLE)
        self.preview.hide()
        
        right_layout.addWidget(tags_widget)
        right_layout.addWidget(self.editor)
        right_layout.addWidget(self.preview)
        
        # Add panels to splitter
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([350, 650])
        
        layout.addWidget(self.splitter)

    def format_text(self):
        fmt = QTextCharFormat()
        fmt.setFont(self.font_family.currentFont())
        fmt.setFontPointSize(self.font_size.value())
        self.editor.textCursor().mergeCharFormat(fmt)
    
    def refresh_note_list(self, notes):
        self.note_list.clear()
        for note in notes:
            item = QListWidgetItem(f"📝 {note.title}")
            item.setData(Qt.UserRole, note.id)
            # Add metadata as tooltip
            created = note.created_at.strftime("%Y-%m-%d %H:%M")
            updated = note.updated_at.strftime("%Y-%m-%d %H:%M")
            item.setToolTip(f"Created: {created}\nLast modified: {updated}")
            self.note_list.addItem(item)
    
    def set_note_content(self, title, content, tags, metadata=None):
        self.editor.setText(content)
        self.tags_input.setText(tags or "")
        if metadata:
            created = metadata['created_at'].strftime("%Y-%m-%d %H:%M")
            updated = metadata['updated_at'].strftime("%Y-%m-%d %H:%M")
            self.metadata_label.setText(f"Created: {created} | Last modified: {updated}")
        else:
            self.metadata_label.clear()
    
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