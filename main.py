import sys
from PySide6.QtWidgets import QApplication, QFileDialog, QColorDialog, QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QTextCharFormat, QColor
import markdown
import json
from database import Database, NoteCategory
from ui.main_window import MainWindow

class NoteTypewriter:
    def __init__(self):
        self.db = Database()
        self.window = MainWindow()
        
        # Connect signals
        self.window.note_selected.connect(self.load_note)
        self.window.note_deleted.connect(self.delete_note)
        self.window.search_changed.connect(self.search_notes)
        self.window.category_changed.connect(self.change_category)
        
        # Connect button signals
        self.window.btn_new.clicked.connect(self.new_note)
        self.window.btn_save.clicked.connect(self.save_note)
        self.window.btn_delete.clicked.connect(self.delete_current_note)
        self.window.btn_toggle_preview.clicked.connect(self.toggle_preview)
        self.window.btn_export.clicked.connect(self.export_note)
        
        # Connect formatting signals
        self.window.btn_bold.clicked.connect(lambda: self.format_text('bold'))
        self.window.btn_italic.clicked.connect(lambda: self.format_text('italic'))
        self.window.btn_underline.clicked.connect(lambda: self.format_text('underline'))
        self.window.btn_color.clicked.connect(self.choose_color)
        
        # Set up auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
        
        # Initialize state
        self.current_note = None
        self.current_category = NoteCategory.ALL
        
        # Load existing notes
        self.refresh_notes()
    
    def refresh_notes(self):
        notes = self.db.get_all_notes(category=self.current_category)
        self.window.refresh_note_list(notes)
    
    def new_note(self):
        from PySide6.QtWidgets import QInputDialog
        title, ok = QInputDialog.getText(self.window, "New Note", "Enter note title:")
        if ok and title:
            note = self.db.create_note(
                title=title,
                category=self.current_category
            )
            self.refresh_notes()
            self.load_note(note.id)
    
    def load_note(self, note_id):
        note = self.db.get_note(note_id)
        if note:
            self.current_note = note
            self.window.set_note_content(
                note.title,
                note.content,
                note.tags,
                metadata={
                    'created_at': note.created_at,
                    'updated_at': note.updated_at
                }
            )
            if note.html_content:
                self.window.editor.setHtml(note.html_content)
    
    def save_note(self):
        if self.current_note:
            content = self.window.get_note_content()
            html_content = self.window.editor.toHtml()
            self.db.update_note(
                self.current_note.id,
                content=content,
                html_content=html_content,
                tags=self.window.get_note_tags()
            )
            self.refresh_notes()
    
    def auto_save(self):
        if self.current_note and self.window.editor.document().isModified():
            self.save_note()
    
    def delete_current_note(self):
        if self.current_note:
            self.delete_note(self.current_note.id)
    
    def delete_note(self, note_id):
        reply = QMessageBox.question(
            self.window, "Delete Note",
            "Are you sure you want to delete this note?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db.delete_note(note_id)
            self.current_note = None
            self.window.editor.clear()
            self.window.tags_input.clear()
            self.refresh_notes()
    
    def search_notes(self, query):
        notes = self.db.search_notes(query, category=self.current_category)
        self.window.refresh_note_list(notes)
    
    def change_category(self, category_name):
        try:
            self.current_category = NoteCategory(category_name)
        except ValueError:
            self.current_category = NoteCategory.ALL
        self.refresh_notes()
    
    def toggle_preview(self):
        content = self.window.get_note_content()
        html = markdown.markdown(content)
        self.window.toggle_preview(html)
    
    def format_text(self, format_type):
        cursor = self.window.editor.textCursor()
        char_format = cursor.charFormat()
        
        if format_type == 'bold':
            char_format.setFontWeight(
                700 if not char_format.fontWeight() == 700 else 400
            )
        elif format_type == 'italic':
            char_format.setFontItalic(not char_format.fontItalic())
        elif format_type == 'underline':
            char_format.setFontUnderline(not char_format.fontUnderline())
        
        cursor.mergeCharFormat(char_format)
        self.window.editor.setTextCursor(cursor)
    
    def choose_color(self):
        color = QColorDialog.getColor(
            initial=QColor('white'),
            parent=self.window,
            title="Choose Text Color"
        )
        if color.isValid():
            cursor = self.window.editor.textCursor()
            fmt = cursor.charFormat()
            fmt.setForeground(color)
            cursor.mergeCharFormat(fmt)
    
    def export_note(self):
        if not self.current_note:
            return
        
        file_name, _ = QFileDialog.getSaveFileName(
            self.window,
            "Export Note",
            "",
            "Markdown Files (*.md);;HTML Files (*.html);;All Files (*)"
        )
        
        if file_name:
            format_type = "html" if file_name.endswith('.html') else "markdown"
            note_data = self.db.export_note(self.current_note.id, format=format_type)
            
            if note_data:
                try:
                    with open(file_name, 'w', encoding='utf-8') as f:
                        if format_type == "markdown":
                            f.write(f"# {note_data['title']}\n\n")
                            f.write(note_data['content'])
                        else:
                            f.write(f"<h1>{note_data['title']}</h1>\n")
                            f.write(note_data['content'])
                    
                    QMessageBox.information(
                        self.window,
                        "Success",
                        f"Note exported successfully to {file_name}"
                    )
                except Exception as e:
                    QMessageBox.warning(
                        self.window,
                        "Error",
                        f"Failed to export note: {str(e)}"
                    )

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    note_app = NoteTypewriter()
    note_app.window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 