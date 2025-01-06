from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
import enum
import json

Base = declarative_base()

class NoteCategory(enum.Enum):
    ALL = "All Notes"
    PERSONAL = "Personal"
    WORK = "Work"
    IDEAS = "Ideas"
    TASKS = "Tasks"

class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    html_content = Column(Text, nullable=True)  # Store formatted content
    category = Column(Enum(NoteCategory), default=NoteCategory.ALL)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    note_metadata = Column(Text, nullable=True)  # JSON string for additional metadata

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'html_content': self.html_content,
            'category': self.category.value if self.category else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'tags': self.tags,
            'metadata': json.loads(self.note_metadata) if self.note_metadata else {}
        }

class Database:
    def __init__(self):
        db_path = os.path.join(os.path.expanduser("~"), ".note_typewriter")
        os.makedirs(db_path, exist_ok=True)
        db_file = os.path.join(db_path, "notes.db")
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def create_note(self, title, content="", html_content="", category=NoteCategory.ALL, tags="", metadata=None):
        note = Note(
            title=title,
            content=content,
            html_content=html_content,
            category=category,
            tags=tags,
            note_metadata=json.dumps(metadata) if metadata else None
        )
        self.session.add(note)
        self.session.commit()
        return note
    
    def get_note(self, note_id):
        return self.session.query(Note).filter(Note.id == note_id).first()
    
    def get_all_notes(self, category=None):
        query = self.session.query(Note)
        if category and category != NoteCategory.ALL:
            query = query.filter(Note.category == category)
        return query.order_by(Note.updated_at.desc()).all()
    
    def update_note(self, note_id, title=None, content=None, html_content=None,
                   category=None, tags=None, metadata=None):
        note = self.get_note(note_id)
        if note:
            if title is not None:
                note.title = title
            if content is not None:
                note.content = content
            if html_content is not None:
                note.html_content = html_content
            if category is not None:
                note.category = category
            if tags is not None:
                note.tags = tags
            if metadata is not None:
                current_metadata = json.loads(note.note_metadata) if note.note_metadata else {}
                current_metadata.update(metadata)
                note.note_metadata = json.dumps(current_metadata)
            self.session.commit()
        return note
    
    def delete_note(self, note_id):
        note = self.get_note(note_id)
        if note:
            self.session.delete(note)
            self.session.commit()
            return True
        return False
    
    def search_notes(self, query, category=None):
        db_query = self.session.query(Note)
        if category and category != NoteCategory.ALL:
            db_query = db_query.filter(Note.category == category)
        
        return db_query.filter(
            (Note.title.ilike(f"%{query}%")) |
            (Note.content.ilike(f"%{query}%")) |
            (Note.tags.ilike(f"%{query}%"))
        ).order_by(Note.updated_at.desc()).all()
    
    def export_note(self, note_id, format="markdown"):
        note = self.get_note(note_id)
        if not note:
            return None
        
        if format == "markdown":
            return {
                'title': note.title,
                'content': note.content,
                'metadata': note.to_dict()
            }
        elif format == "html":
            return {
                'title': note.title,
                'content': note.html_content or note.content,
                'metadata': note.to_dict()
            }
        return None
    
    def import_note(self, data):
        try:
            title = data.get('title', 'Imported Note')
            content = data.get('content', '')
            metadata = data.get('metadata', {})
            category = metadata.get('category', NoteCategory.ALL)
            tags = metadata.get('tags', '')
            
            return self.create_note(
                title=title,
                content=content,
                category=category,
                tags=tags,
                metadata=metadata
            )
        except Exception as e:
            print(f"Error importing note: {e}")
            return None 