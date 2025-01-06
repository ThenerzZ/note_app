from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(String(500), nullable=True)  # Comma-separated tags

class Database:
    def __init__(self):
        db_path = os.path.join(os.path.expanduser("~"), ".note_typewriter")
        os.makedirs(db_path, exist_ok=True)
        db_file = os.path.join(db_path, "notes.db")
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def create_note(self, title, content="", tags=""):
        note = Note(title=title, content=content, tags=tags)
        self.session.add(note)
        self.session.commit()
        return note
    
    def get_note(self, note_id):
        return self.session.query(Note).filter(Note.id == note_id).first()
    
    def get_all_notes(self):
        return self.session.query(Note).order_by(Note.updated_at.desc()).all()
    
    def update_note(self, note_id, title=None, content=None, tags=None):
        note = self.get_note(note_id)
        if note:
            if title is not None:
                note.title = title
            if content is not None:
                note.content = content
            if tags is not None:
                note.tags = tags
            self.session.commit()
        return note
    
    def delete_note(self, note_id):
        note = self.get_note(note_id)
        if note:
            self.session.delete(note)
            self.session.commit()
            return True
        return False
    
    def search_notes(self, query):
        return self.session.query(Note).filter(
            (Note.title.ilike(f"%{query}%")) |
            (Note.content.ilike(f"%{query}%")) |
            (Note.tags.ilike(f"%{query}%"))
        ).order_by(Note.updated_at.desc()).all() 