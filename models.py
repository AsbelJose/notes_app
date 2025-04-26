
''' ¿Cómo crear modelos y tablas con SQLAlchemy?
Los modelos en SQLAlchemy son clases de Python que representan tablas en la base de datos. Cada atributo de la clase corresponde a 
una columna en la tabla.

Para nuestro ejemplo, crearemos un modelo Note para almacenar notas con título y contenido: '''

from flask_sqlalchemy import SQLAlchemy


# Instancia de SQLAlchemy
db = SQLAlchemy()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    def __repr__(self):
        return f'Note {self.id}: {self.title}'

'''En este modelo:

id: Es un entero que actúa como clave primaria
title: Es una cadena de texto con longitud máxima de 100 caracteres y no puede ser nula
content: Es una cadena de texto con longitud máxima de 200 caracteres y tampoco puede ser nula
El método __repr__ define cómo se mostrará el objeto cuando se imprima '''