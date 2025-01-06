from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QTextEdit, QLineEdit,
                             QSplitter, QLabel, QListWidgetItem, QToolBar,
                             QFontComboBox, QSpinBox, QComboBox, QFrame,
                             QMenu, QToolButton, QMenuBar, QStatusBar)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import (QIcon, QFont, QKeySequence, QTextCharFormat,
                        QColor, QTextCursor, QAction, QFontDatabase,
                        QTextListFormat, QTextBlockFormat)
from .styles import *
from .enhanced_editor import EnhancedEditor

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
    
    def value(self):
        try:
            return float(self.currentText())
        except ValueError:
            return 11.0
        
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
        # We'll remove this method since we're handling shortcuts in the menu bar
        pass

    def setup_ui(self):
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet(SPLITTER_STYLE)
        
        # Left panel (Navigation)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(5)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # Search and category in one toolbar
        nav_toolbar = QFrame()
        nav_toolbar.setStyleSheet(NAV_TOOLBAR_STYLE)
        nav_layout = QVBoxLayout(nav_toolbar)
        nav_layout.setSpacing(6)
        nav_layout.setContentsMargins(8, 8, 8, 8)
        
        # Category selector
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet(COMBOBOX_STYLE)
        self.category_combo.addItems(["📁 All Notes", "👤 Personal", "💼 Work", "💡 Ideas", "✅ Tasks"])
        self.category_combo.currentTextChanged.connect(
            lambda t: self.category_changed.emit(t.split(" ", 1)[1])
        )
        self.category_combo.setMinimumWidth(200)
        self.category_combo.setFixedHeight(28)  # Consistent height
        
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search notes...")
        self.search_bar.setStyleSheet(SEARCH_BAR_STYLE)
        self.search_bar.textChanged.connect(self.search_changed.emit)
        self.search_bar.setFixedHeight(28)  # Consistent height
        
        nav_layout.addWidget(self.category_combo)
        nav_layout.addWidget(self.search_bar)
        
        # Note list
        self.note_list = QListWidget()
        self.note_list.setStyleSheet(NOTE_LIST_STYLE)
        self.note_list.itemClicked.connect(
            lambda item: self.note_selected.emit(item.data(Qt.UserRole))
        )
        
        left_layout.addWidget(nav_toolbar)
        left_layout.addWidget(self.note_list)
        
        # Right panel (Editor)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(0)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Format toolbar
        format_toolbar = QFrame()
        format_toolbar.setStyleSheet(TOOLBAR_STYLE)
        format_layout = QHBoxLayout(format_toolbar)
        format_layout.setContentsMargins(4, 0, 4, 0)  # Minimal margins
        format_layout.setSpacing(1)  # Minimal spacing
        
        # Font controls in a more compact layout
        self.font_family = QFontComboBox()
        self.font_family.setStyleSheet(COMBOBOX_STYLE)
        self.font_family.currentFontChanged.connect(self.format_font)
        self.font_family.setFixedWidth(100)  # Even smaller width
        
        self.font_size = FontSizeComboBox()
        self.font_size.currentTextChanged.connect(self.format_font_size)
        self.font_size.setFixedWidth(40)  # Even smaller width
        
        # Format buttons in a more compact layout
        format_layout.addWidget(self.font_family)
        format_layout.addWidget(self.font_size)
        format_layout.addWidget(create_small_separator())
        
        # Text style buttons
        self.btn_bold = FormatToolButton("Bold", "B", "Bold (Ctrl+B)")
        self.btn_italic = FormatToolButton("Italic", "I", "Italic (Ctrl+I)")
        self.btn_underline = FormatToolButton("Underline", "U", "Underline (Ctrl+U)")
        
        for btn in [self.btn_bold, self.btn_italic, self.btn_underline]:
            btn.setFixedSize(20, 20)  # Smaller buttons
            format_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, b=btn: self.format_text(b.text().lower()))
        
        format_layout.addWidget(create_small_separator())
        
        # Alignment buttons
        self.btn_align_left = FormatToolButton("Left", "⫷", "Align Left")
        self.btn_align_center = FormatToolButton("Center", "⟺", "Center")
        self.btn_align_right = FormatToolButton("Right", "⫸", "Align Right")
        
        for btn in [self.btn_align_left, self.btn_align_center, self.btn_align_right]:
            btn.setFixedSize(20, 20)  # Smaller buttons
            format_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, b=btn: self.align_text(b.text().lower()))
        
        format_layout.addWidget(create_small_separator())
        
        # List buttons
        self.btn_bullet_list = FormatToolButton("Bullet List", "•", "Bullet List")
        self.btn_number_list = FormatToolButton("Number List", "1.", "Number List")
        
        for btn in [self.btn_bullet_list, self.btn_number_list]:
            btn.setFixedSize(20, 20)  # Smaller buttons
            format_layout.addWidget(btn)
        
        self.btn_bullet_list.clicked.connect(lambda: self.make_list('bullet'))
        self.btn_number_list.clicked.connect(lambda: self.make_list('number'))
        
        format_layout.addStretch()
        
        # Tags in a minimal inline layout
        self.tags_label = QLabel("🏷️")
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Add tags...")
        self.tags_input.setStyleSheet(TAGS_STYLE)
        self.tags_input.setFixedWidth(120)  # Smaller width
        self.tags_input.setFixedHeight(20)  # Smaller height
        
        format_layout.addWidget(self.tags_label)
        format_layout.addWidget(self.tags_input)
        format_layout.addWidget(create_small_separator())
        
        # Metadata label
        self.metadata_label = QLabel()
        self.metadata_label.setStyleSheet(METADATA_STYLE)
        format_layout.addWidget(self.metadata_label)
        
        # Editor widget
        self.editor_widget = EnhancedEditor()
        self.editor = self.editor_widget.editor
        self.preview = self.editor_widget.preview
        
        # Connect text change handler
        self.editor.textChanged.connect(self.handle_text_change)
        
        # Add widgets to right layout
        right_layout.addWidget(format_toolbar)
        right_layout.addWidget(self.editor_widget)
        
        # Add panels to splitter
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([250, 750])  # 25% - 75% split
        
        layout.addWidget(self.splitter)
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Create menu bar (after editor_widget is created)
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(MENU_STYLE)
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # Create buttons first
        self.btn_new = QAction("New Note", self)
        self.btn_new.setShortcut(QKeySequence("Ctrl+N"))
        self.btn_new.triggered.connect(self.new_note_requested.emit)
        
        self.btn_save = QAction("Save", self)
        self.btn_save.setShortcut(QKeySequence("Ctrl+S"))
        self.btn_save.triggered.connect(self.save_note_requested.emit)
        
        file_menu.addAction(self.btn_new)
        file_menu.addAction(self.btn_save)
        file_menu.addSeparator()
        
        # Export menu
        export_menu = QMenu("Export As", self)
        self.export_md = export_menu.addAction("Markdown (.md)")
        self.export_html = export_menu.addAction("HTML (.html)")
        self.export_pdf = export_menu.addAction("PDF (.pdf)")
        self.export_docx = export_menu.addAction("Word (.docx)")
        file_menu.addMenu(export_menu)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        # Add search action to Edit menu
        search_action = QAction("Search", self)
        search_action.setShortcut(QKeySequence("Ctrl+F"))
        search_action.triggered.connect(lambda: self.search_bar.setFocus())
        edit_menu.addAction(search_action)
        
        # Format menu
        format_menu = menubar.addMenu("Format")
        
        # Text formatting actions
        bold_action = QAction("Bold", self)
        bold_action.setShortcut(QKeySequence("Ctrl+B"))
        bold_action.triggered.connect(lambda: self.format_text('bold'))
        format_menu.addAction(bold_action)
        
        italic_action = QAction("Italic", self)
        italic_action.setShortcut(QKeySequence("Ctrl+I"))
        italic_action.triggered.connect(lambda: self.format_text('italic'))
        format_menu.addAction(italic_action)
        
        underline_action = QAction("Underline", self)
        underline_action.setShortcut(QKeySequence("Ctrl+U"))
        underline_action.triggered.connect(lambda: self.format_text('underline'))
        format_menu.addAction(underline_action)
        
        format_menu.addSeparator()
        
        # Font size shortcuts
        increase_size = QAction("Increase Font Size", self)
        increase_size.setShortcut(QKeySequence("Ctrl++"))
        increase_size.triggered.connect(self.increase_font_size)
        format_menu.addAction(increase_size)
        
        decrease_size = QAction("Decrease Font Size", self)
        decrease_size.setShortcut(QKeySequence("Ctrl+-"))
        decrease_size.triggered.connect(self.decrease_font_size)
        format_menu.addAction(decrease_size)
        
        format_menu.addSeparator()
        
        # Alignment submenu
        align_menu = format_menu.addMenu("Align")
        align_menu.addAction("Left").triggered.connect(lambda: self.align_text('left'))
        align_menu.addAction("Center").triggered.connect(lambda: self.align_text('center'))
        align_menu.addAction("Right").triggered.connect(lambda: self.align_text('right'))
        
        # List submenu
        list_menu = format_menu.addMenu("List")
        list_menu.addAction("Bullet List").triggered.connect(lambda: self.make_list('bullet'))
        list_menu.addAction("Number List").triggered.connect(lambda: self.make_list('number'))
        
        # Insert menu
        insert_menu = menubar.addMenu("Insert")
        
        insert_menu.addAction("Image").triggered.connect(self.editor_widget.insert_image)
        insert_menu.addAction("Table").triggered.connect(self.editor_widget.insert_table)
        
        code_menu = insert_menu.addMenu("Code Block")
        languages = ["Python", "JavaScript", "HTML", "CSS", "Java", "C++", "SQL", "Bash"]
        for lang in languages:
            code_menu.addAction(lang).triggered.connect(
                lambda checked, l=lang.lower(): self.editor_widget.insert_code_block(l)
            )
        
        insert_menu.addAction("Task Checkbox").triggered.connect(self.insert_checkbox)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        preview_action = QAction("Toggle Preview", self)
        preview_action.setShortcut(QKeySequence("Ctrl+P"))
        preview_action.triggered.connect(self.toggle_preview)
        view_menu.addAction(preview_action)
        
        full_preview_action = QAction("Full Preview", self)
        full_preview_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        full_preview_action.triggered.connect(lambda: self.editor_widget.toggle_preview("full"))
        view_menu.addAction(full_preview_action)
        
        # Connect export actions
        self.export_md.triggered.connect(lambda: self.export_requested.emit("markdown"))
        self.export_html.triggered.connect(lambda: self.export_requested.emit("html"))
        self.export_pdf.triggered.connect(lambda: self.export_requested.emit("pdf"))
        self.export_docx.triggered.connect(lambda: self.export_requested.emit("docx"))

    # Add new signals for menu actions
    new_note_requested = Signal()
    save_note_requested = Signal()
    export_requested = Signal(str)  # Signal with export format parameter

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
    
    def toggle_preview(self):
        self.editor_widget.toggle_preview("split")
    
    def insert_code_block(self):
        languages = ["python", "javascript", "html", "css", "java", "cpp", "sql", "bash"]
        menu = QMenu(self)
        for lang in languages:
            action = menu.addAction(lang.capitalize())
            action.triggered.connect(lambda checked, l=lang: self.editor_widget.insert_code_block(l))
        
        menu.exec_(self.btn_insert_code.mapToGlobal(self.btn_insert_code.rect().bottomLeft()))
    
    def insert_checkbox(self):
        cursor = self.editor.textCursor()
        cursor.insertText("- [ ] ")
    
    def insert_image(self):
        self.editor_widget.insert_image()
    
    def insert_table(self):
        self.editor_widget.insert_table()
    
    def insert_code(self):
        self.editor_widget.insert_code()
    
    def insert_checkbox(self):
        self.editor_widget.insert_checkbox() 

def create_small_separator():
    separator = QFrame()
    separator.setFrameShape(QFrame.VLine)
    separator.setStyleSheet(SEPARATOR_STYLE)
    separator.setFixedHeight(16)  # Even smaller height
    return separator 