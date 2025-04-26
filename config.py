import os


# Configuración de la ruta del archivo de base de datos
DB_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "notes.sqlite"
)

# Configuración de SQLAlchemy
class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "cualquier_valor_secreto"

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_notes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "cualquier_valor_secreto"
    TESTING = True