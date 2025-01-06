from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
                             QTextEdit, QToolButton, QFileDialog, QMenu,
                             QDialog, QLabel, QPushButton)
from PySide6.QtCore import Qt, Signal, QMimeData, QUrl
from PySide6.QtGui import (QTextCharFormat, QImage, QTextCursor,
                        QDropEvent, QDragEnterEvent, QPainter, QColor)
import markdown
from markdown.extensions import fenced_code
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.nl2br import Nl2BrExtension
from markdown.extensions.sane_lists import SaneListExtension
import os
from datetime import datetime
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
import base64
from PIL import Image
from io import BytesIO

class MarkdownPreview(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                padding: 20px;
                background-color: #141414;
                border: none;
                border-radius: 8px;
            }
        """)
        
        # Setup Markdown extensions
        self.md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
            'markdown.extensions.meta',
            'markdown.extensions.footnotes',
            CodeHiliteExtension(css_class='highlight'),
            TableExtension(),
            TocExtension(permalink=True)
        ])
        
        # Add CSS for syntax highlighting
        self.css = HtmlFormatter().get_style_defs('.highlight')
        
    def update_preview(self, text):
        # Convert Markdown to HTML
        html = self.md.convert(text)
        
        # Add custom CSS
        styled_html = f"""
        <style>
            body {{
                font-family: 'SF Pro Text', 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #ffffff;
                background-color: #141414;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #ff69b4;
                border-bottom: 1px solid #2d2d2d;
                padding-bottom: 5px;
            }}
            code {{
                background-color: #1f1f1f;
                padding: 2px 4px;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
            }}
            pre {{
                background-color: #1f1f1f;
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
            }}
            blockquote {{
                border-left: 4px solid #ff69b4;
                margin: 0;
                padding-left: 15px;
                color: #e0e0e0;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
            }}
            th, td {{
                border: 1px solid #2d2d2d;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #1f1f1f;
                color: #ff69b4;
            }}
            img {{
                max-width: 100%;
                border-radius: 8px;
            }}
            {self.css}
        </style>
        {html}
        """
        self.setHtml(styled_html)

class EnhancedEditor(QWidget):
    content_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Create splitter for editor and preview
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Editor
        self.editor = QTextEdit()
        self.editor.setAcceptRichText(True)
        self.editor.textChanged.connect(self.handle_content_changed)
        self.editor.setStyleSheet("""
            QTextEdit {
                padding: 20px;
                background-color: #141414;
                border: none;
                border-radius: 8px;
                color: #ffffff;
                font-family: 'SF Pro Text', 'Segoe UI', Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.6;
            }
        """)
        
        # Preview
        self.preview = MarkdownPreview()
        self.preview.hide()  # Initially hidden
        
        # Add widgets to splitter
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.preview)
        
        # Add splitter to layout
        layout.addWidget(self.splitter)
        
        # Setup drag and drop
        self.editor.setAcceptDrops(True)
        self.editor.dragEnterEvent = self.dragEnterEvent
        self.editor.dropEvent = self.dropEvent
        
    def handle_content_changed(self):
        self.content_changed.emit()
        if not self.preview.isHidden():
            self.preview.update_preview(self.editor.toPlainText())
    
    def toggle_preview(self, preview_type="split"):
        if preview_type == "split":
            if self.preview.isHidden():
                self.preview.show()
                self.preview.update_preview(self.editor.toPlainText())
                self.splitter.setSizes([self.width() // 2, self.width() // 2])
            else:
                self.preview.hide()
                self.splitter.setSizes([self.width(), 0])
        else:  # full preview
            if self.preview.isHidden():
                self.editor.hide()
                self.preview.show()
                self.preview.update_preview(self.editor.toPlainText())
            else:
                self.preview.hide()
                self.editor.show()
    
    def insert_image(self, image_path=None):
        if not image_path:
            image_path, _ = QFileDialog.getOpenFileName(
                self, "Insert Image", "",
                "Images (*.png *.jpg *.jpeg *.gif *.bmp)"
            )
        
        if image_path:
            # Convert image to base64
            with open(image_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            # Insert markdown image
            cursor = self.editor.textCursor()
            image_name = os.path.basename(image_path)
            cursor.insertText(f"\n![{image_name}](data:image/png;base64,{img_data})\n")
    
    def insert_table(self, rows=3, cols=3):
        # Create markdown table
        header = "|" + "|".join(" Header " for _ in range(cols)) + "|\n"
        separator = "|" + "|".join(" --- " for _ in range(cols)) + "|\n"
        rows_text = ""
        for _ in range(rows-1):
            rows_text += "|" + "|".join(" Cell " for _ in range(cols)) + "|\n"
        
        table = f"\n{header}{separator}{rows_text}\n"
        
        # Insert at cursor position
        cursor = self.editor.textCursor()
        cursor.insertText(table)
    
    def insert_code_block(self, language="python"):
        template = f"\n```{language}\n# Your code here\n```\n"
        cursor = self.editor.textCursor()
        cursor.insertText(template)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and any(url.toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
                                     for url in mime_data.urls()):
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.insert_image(file_path)
                break 
    
    def insert_checkbox(self):
        cursor = self.editor.textCursor()
        cursor.insertText("- [ ] ")
        self.editor.setFocus() 