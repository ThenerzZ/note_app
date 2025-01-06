from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QTextEdit, QLineEdit,
                             QSplitter, QLabel, QListWidgetItem, QToolBar,
                             QFontComboBox, QSpinBox, QComboBox, QFrame,
                             QMenu, QToolButton)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import (QIcon, QFont, QKeySequence, QTextCharFormat,
                        QColor, QTextCursor, QAction, QFontDatabase,
                        QTextListFormat, QTextBlockFormat)
from .styles import *

# Preset font sizes that match common text editors
FONT_SIZES = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]

class FontSizeComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setStyleSheet(COMBOBOX_STYLE)
        self.setFixedWidth(70)
        
        # Add preset sizes
        for size in FONT_SIZES:
            self.addItem(str(size))
        
        # Set default size
        self.setCurrentText("11")
        
        # Connect signals
        self.currentTextChanged.connect(self.validate_size)
        
    def validate_size(self, text):
        try:
            size = int(text)
            if size < 1:
                self.setCurrentText("1")
            elif size > 72:
                self.setCurrentText("72")
        except ValueError:
            # If invalid input, revert to previous valid size
            self.setCurrentText("11")

class RichTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(True)
        self.setTabStopDistance(20)
        
        # Set default font
        font = QFont("Segoe UI", 11)
        self.setFont(font)
        
        # Set line wrap mode
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Set default paragraph spacing and line height
        block_format = QTextBlockFormat()
        block_format.setLineHeight(150, 1)  # 150% line height, type 1 = ProportionalHeight
        block_format.setTopMargin(8)
        block_format.setBottomMargin(8)
        
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.mergeBlockFormat(block_format)
        self.setTextCursor(cursor)
        
        # Set as default format for new blocks
        self.document().setDefaultTextOption(self.document().defaultTextOption())
        self.setCurrentCharFormat(QTextCharFormat())

class FormatToolButton(QToolButton):
    def __init__(self, text, icon_text, tooltip, parent=None):
        super().__init__(parent)
        self.setText(icon_text)
        self.setToolTip(tooltip)
        self.setCheckable(True)
        self.setAutoRaise(True)
        self.setStyleSheet(TOOL_BUTTON_STYLE)
        self.setFixedSize(32, 32)

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

        # Text formatting shortcuts
        bold_shortcut = QAction("Bold", self)
        bold_shortcut.setShortcut(QKeySequence.Bold)
        bold_shortcut.triggered.connect(lambda: self.format_text('bold'))
        self.addAction(bold_shortcut)

        italic_shortcut = QAction("Italic", self)
        italic_shortcut.setShortcut(QKeySequence.Italic)
        italic_shortcut.triggered.connect(lambda: self.format_text('italic'))
        self.addAction(italic_shortcut)

        underline_shortcut = QAction("Underline", self)
        underline_shortcut.setShortcut(QKeySequence.Underline)
        underline_shortcut.triggered.connect(lambda: self.format_text('underline'))
        self.addAction(underline_shortcut)

        # Add font size shortcuts
        increase_size = QAction("Increase Font Size", self)
        increase_size.setShortcut(QKeySequence("Ctrl++"))
        increase_size.triggered.connect(self.increase_font_size)
        self.addAction(increase_size)

        decrease_size = QAction("Decrease Font Size", self)
        decrease_size.setShortcut(QKeySequence("Ctrl+-"))
        decrease_size.triggered.connect(self.decrease_font_size)
        self.addAction(decrease_size)

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
        
        # Category selector with label
        category_widget = QWidget()
        category_layout = QHBoxLayout(category_widget)
        category_layout.setContentsMargins(0, 0, 0, 0)
        
        category_label = QLabel("📂 Category:")
        category_label.setStyleSheet(LABEL_STYLE)
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet(COMBOBOX_STYLE)
        self.category_combo.addItems(["All Notes", "Personal", "Work", "Ideas", "Tasks"])
        self.category_combo.currentTextChanged.connect(self.category_changed.emit)
        
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        left_layout.addWidget(category_widget)
        
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
        
        # Main toolbar
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
        
        toolbar_layout.addStretch()
        
        # Formatting toolbar
        format_toolbar = QFrame()
        format_toolbar.setStyleSheet(TOOLBAR_STYLE)
        format_layout = QHBoxLayout(format_toolbar)
        format_layout.setContentsMargins(10, 5, 10, 5)
        format_layout.setSpacing(8)

        # Style section
        style_section = QFrame()
        style_layout = QHBoxLayout(style_section)
        style_layout.setContentsMargins(0, 0, 0, 0)
        style_layout.setSpacing(4)

        # Font controls
        font_controls = QWidget()
        font_layout = QHBoxLayout(font_controls)
        font_layout.setContentsMargins(0, 0, 0, 0)
        font_layout.setSpacing(4)

        # Font family with label
        font_label = QLabel("Font:")
        font_label.setStyleSheet(TOOLBAR_LABEL_STYLE)
        self.font_family = QFontComboBox()
        self.font_family.setStyleSheet(COMBOBOX_STYLE)
        self.font_family.currentFontChanged.connect(self.format_font)
        self.font_family.setFixedWidth(180)
        
        # Font size with label
        size_label = QLabel("Size:")
        size_label.setStyleSheet(TOOLBAR_LABEL_STYLE)
        self.font_size = FontSizeComboBox()
        self.font_size.currentTextChanged.connect(self.format_font_size)
        
        # Add decrease/increase font size buttons
        self.btn_decrease_size = FormatToolButton("Decrease size", "A-", "Decrease font size (Ctrl+-)")
        self.btn_decrease_size.setCheckable(False)
        self.btn_increase_size = FormatToolButton("Increase size", "A+", "Increase font size (Ctrl++)")
        self.btn_increase_size.setCheckable(False)
        
        self.btn_decrease_size.clicked.connect(self.decrease_font_size)
        self.btn_increase_size.clicked.connect(self.increase_font_size)

        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_family)
        font_layout.addSpacing(10)
        font_layout.addWidget(size_label)
        font_layout.addWidget(self.font_size)
        font_layout.addWidget(self.btn_decrease_size)
        font_layout.addWidget(self.btn_increase_size)
        
        style_layout.addWidget(font_controls)
        format_layout.addWidget(style_section)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet(SEPARATOR_STYLE)
        format_layout.addWidget(separator)

        # Text format section
        format_section = QFrame()
        format_layout_inner = QHBoxLayout(format_section)
        format_layout_inner.setContentsMargins(0, 0, 0, 0)
        format_layout_inner.setSpacing(4)

        # Format buttons with better icons
        self.btn_bold = FormatToolButton("Bold", "B", "Bold (Ctrl+B)")
        self.btn_italic = FormatToolButton("Italic", "I", "Italic (Ctrl+I)")
        self.btn_underline = FormatToolButton("Underline", "U", "Underline (Ctrl+U)")
        
        # Text alignment buttons
        self.btn_align_left = FormatToolButton("Left", "⫷", "Align Left")
        self.btn_align_center = FormatToolButton("Center", "⟺", "Center")
        self.btn_align_right = FormatToolButton("Right", "⫸", "Align Right")
        
        # List buttons
        self.btn_bullet_list = FormatToolButton("Bullet List", "•", "Bullet List")
        self.btn_number_list = FormatToolButton("Number List", "1.", "Number List")

        # Add all format buttons
        for btn in [self.btn_bold, self.btn_italic, self.btn_underline]:
            format_layout_inner.addWidget(btn)
        
        # Add separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.VLine)
        separator2.setStyleSheet(SEPARATOR_STYLE)
        format_layout_inner.addWidget(separator2)

        # Add alignment buttons
        for btn in [self.btn_align_left, self.btn_align_center, self.btn_align_right]:
            format_layout_inner.addWidget(btn)

        # Add separator
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.VLine)
        separator3.setStyleSheet(SEPARATOR_STYLE)
        format_layout_inner.addWidget(separator3)

        # Add list buttons
        for btn in [self.btn_bullet_list, self.btn_number_list]:
            format_layout_inner.addWidget(btn)

        format_layout.addWidget(format_section)
        format_layout.addStretch()

        # Connect format buttons
        self.btn_bold.clicked.connect(lambda: self.format_text('bold'))
        self.btn_italic.clicked.connect(lambda: self.format_text('italic'))
        self.btn_underline.clicked.connect(lambda: self.format_text('underline'))
        self.btn_align_left.clicked.connect(lambda: self.align_text('left'))
        self.btn_align_center.clicked.connect(lambda: self.align_text('center'))
        self.btn_align_right.clicked.connect(lambda: self.align_text('right'))
        self.btn_bullet_list.clicked.connect(lambda: self.make_list('bullet'))
        self.btn_number_list.clicked.connect(lambda: self.make_list('number'))

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
        
        # Editor and metadata
        self.metadata_label = QLabel()
        self.metadata_label.setStyleSheet(METADATA_STYLE)
        
        # Text editor (using custom RichTextEdit)
        self.editor = RichTextEdit()
        self.editor.setStyleSheet(EDITOR_STYLE)
        self.editor.textChanged.connect(self.handle_text_change)
        
        # Preview widget
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setStyleSheet(EDITOR_STYLE)
        self.preview.hide()
        
        # Add all widgets to right layout
        right_layout.addWidget(toolbar)
        right_layout.addWidget(format_toolbar)
        right_layout.addWidget(tags_widget)
        right_layout.addWidget(self.metadata_label)
        right_layout.addWidget(self.editor)
        right_layout.addWidget(self.preview)
        
        # Add panels to splitter
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([350, 650])
        
        layout.addWidget(self.splitter)

    def format_text(self, format_type):
        cursor = self.editor.textCursor()
        fmt = QTextCharFormat()
        
        if format_type == 'bold':
            fmt.setFontWeight(QFont.Bold if not cursor.charFormat().fontWeight() == QFont.Bold else QFont.Normal)
        elif format_type == 'italic':
            fmt.setFontItalic(not cursor.charFormat().fontItalic())
        elif format_type == 'underline':
            fmt.setFontUnderline(not cursor.charFormat().fontUnderline())
        
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)
        self.editor.setFocus()

    def align_text(self, alignment):
        cursor = self.editor.textCursor()
        block_fmt = cursor.blockFormat()
        
        if alignment == 'left':
            block_fmt.setAlignment(Qt.AlignLeft)
            self.btn_align_left.setChecked(True)
            self.btn_align_center.setChecked(False)
            self.btn_align_right.setChecked(False)
        elif alignment == 'center':
            block_fmt.setAlignment(Qt.AlignCenter)
            self.btn_align_left.setChecked(False)
            self.btn_align_center.setChecked(True)
            self.btn_align_right.setChecked(False)
        elif alignment == 'right':
            block_fmt.setAlignment(Qt.AlignRight)
            self.btn_align_left.setChecked(False)
            self.btn_align_center.setChecked(False)
            self.btn_align_right.setChecked(True)
        
        cursor.mergeBlockFormat(block_fmt)
        self.editor.setFocus()

    def make_list(self, list_type):
        cursor = self.editor.textCursor()
        list_fmt = QTextListFormat()
        
        if list_type == 'bullet':
            list_fmt.setStyle(QTextListFormat.ListDisc)
            self.btn_bullet_list.setChecked(not self.btn_bullet_list.isChecked())
            self.btn_number_list.setChecked(False)
        else:
            list_fmt.setStyle(QTextListFormat.ListDecimal)
            self.btn_number_list.setChecked(not self.btn_number_list.isChecked())
            self.btn_bullet_list.setChecked(False)
        
        cursor.createList(list_fmt)
        self.editor.setFocus()

    def handle_text_change(self):
        cursor = self.editor.textCursor()
        fmt = cursor.charFormat()
        block_fmt = cursor.blockFormat()
        
        # Update format buttons state
        self.btn_bold.setChecked(fmt.fontWeight() == QFont.Bold)
        self.btn_italic.setChecked(fmt.fontItalic())
        self.btn_underline.setChecked(fmt.fontUnderline())
        
        # Update alignment buttons
        alignment = block_fmt.alignment()
        self.btn_align_left.setChecked(alignment == Qt.AlignLeft)
        self.btn_align_center.setChecked(alignment == Qt.AlignCenter)
        self.btn_align_right.setChecked(alignment == Qt.AlignRight)
        
        # Update list buttons
        current_list = cursor.currentList()
        if current_list:
            list_fmt = current_list.format()
            self.btn_bullet_list.setChecked(list_fmt.style() == QTextListFormat.ListDisc)
            self.btn_number_list.setChecked(list_fmt.style() == QTextListFormat.ListDecimal)
        else:
            self.btn_bullet_list.setChecked(False)
            self.btn_number_list.setChecked(False)
        
        # Update font controls
        if fmt.fontPointSize() > 0:
            self.font_size.setValue(int(fmt.fontPointSize()))
        self.font_family.setCurrentFont(fmt.font())

    def format_font(self):
        cursor = self.editor.textCursor()
        fmt = cursor.charFormat()
        fmt.setFont(self.font_family.currentFont())
        fmt.setFontPointSize(self.font_size.value())
        
        if cursor.hasSelection():
            cursor.mergeCharFormat(fmt)
        else:
            self.editor.setCurrentCharFormat(fmt)
        
        self.editor.setFocus()

    def format_font_size(self):
        try:
            size = float(self.font_size.currentText())
            cursor = self.editor.textCursor()
            fmt = QTextCharFormat()
            fmt.setFontPointSize(size)
            
            if cursor.hasSelection():
                cursor.mergeCharFormat(fmt)
            else:
                self.editor.setCurrentCharFormat(fmt)
            
            self.editor.setFocus()
        except ValueError:
            pass

    def decrease_font_size(self):
        current_size = float(self.font_size.currentText())
        new_size = current_size
        
        # Find the next smaller size in presets
        for size in reversed(FONT_SIZES):
            if size < current_size:
                new_size = size
                break
        
        self.font_size.setCurrentText(str(new_size))
        self.format_font_size()

    def increase_font_size(self):
        current_size = float(self.font_size.currentText())
        new_size = current_size
        
        # Find the next larger size in presets
        for size in FONT_SIZES:
            if size > current_size:
                new_size = size
                break
        
        self.font_size.setCurrentText(str(new_size))
        self.format_font_size()

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