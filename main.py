import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
import markdown
from database import Database
from ui.main_window import MainWindow

class NoteTypewriter:
    def __init__(self):
        self.db = Database()
        self.window = MainWindow()
        
        # Connect signals
        self.window.note_selected.connect(self.load_note)
        self.window.note_deleted.connect(self.delete_note)
        self.window.search_changed.connect(self.search_notes)
        
        # Connect button signals
        self.window.btn_new.clicked.connect(self.new_note)
        self.window.btn_save.clicked.connect(self.save_note)
        self.window.btn_delete.clicked.connect(self.delete_current_note)
        self.window.btn_toggle_preview.clicked.connect(self.toggle_preview)
        
        # Set up auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
        
        # Initialize state
        self.current_note = None
        
        # Load existing notes
        self.refresh_notes()
    
    def refresh_notes(self):
        notes = self.db.get_all_notes()
        self.window.refresh_note_list(notes)
    
    def new_note(self):
        from PySide6.QtWidgets import QInputDialog
        title, ok = QInputDialog.getText(self.window, "New Note", "Enter note title:")
        if ok and title:
            note = self.db.create_note(title)
            self.refresh_notes()
            self.load_note(note.id)
    
    def load_note(self, note_id):
        note = self.db.get_note(note_id)
        if note:
            self.current_note = note
            self.window.set_note_content(note.title, note.content, note.tags)
    
    def save_note(self):
        if self.current_note:
            self.db.update_note(
                self.current_note.id,
                content=self.window.get_note_content(),
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
        from PySide6.QtWidgets import QMessageBox
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
        notes = self.db.search_notes(query) if query else self.db.get_all_notes()
        self.window.refresh_note_list(notes)
    
    def toggle_preview(self):
        content = self.window.get_note_content()
        html = markdown.markdown(content)
        self.window.toggle_preview(html)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    note_app = NoteTypewriter()
    note_app.window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 