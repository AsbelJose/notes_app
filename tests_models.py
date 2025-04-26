import unittest
from app import create_app
from config import TestConfig
from models import db, Note

class NoteModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def test_create_note(self):
        with self.app.app_context():
            note = Note(title="Título", content="Contenido")
            db.session.add(note)
            db.session.commit()
            
            saved_note = Note.query.first()
            
            self.assertEqual(saved_note.title, "Título")
            self.assertEqual(saved_note.content, "Contenido")