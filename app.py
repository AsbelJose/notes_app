
from flask import Flask, request, jsonify, render_template, redirect, url_for


app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy

# Configuración de la ruta del archivo de base de datos
DB_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "notes.sqlite"
)

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instancia de SQLAlchemy
db = SQLAlchemy(app)

''' ¿Cómo crear modelos y tablas con SQLAlchemy?
Los modelos en SQLAlchemy son clases de Python que representan tablas en la base de datos. Cada atributo de la clase corresponde a 
una columna en la tabla.

Para nuestro ejemplo, crearemos un modelo Note para almacenar notas con título y contenido: '''

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'Note {self.id}: {self.title}'

'''En este modelo:

id: Es un entero que actúa como clave primaria
title: Es una cadena de texto con longitud máxima de 100 caracteres y no puede ser nula
content: Es una cadena de texto con longitud máxima de 200 caracteres y tampoco puede ser nula
El método __repr__ define cómo se mostrará el objeto cuando se imprima '''


@app.route("/")
def home():
    notes = Note.query.all() # obtiene todas las notas de la base de datos.
    return render_template("home.html", notes=notes )

@app.route("/acerca-de")
def about():
    return "Esto es una app de notas"

@app.route("/contacto", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        return "Formulario enviado correctamente"
    return "pagina de contacto"

# retornando un json.
@app.route("/api/info")
def api_info():
    data = {
        "nombre": "Notes App",
        "version": "1.1.1"
    }
    return jsonify(data), 200

@app.route("/confirmacion")
def confirmation():
    return "prueba"

@app.route("/crear-nota", methods=["GET", "POST"])
def create_note():

    if request.method == "POST":
        # Obtiene los datos del formulario (título y contenido)
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        # Crea una nueva instancia del modelo Note con esos datos
        note_db = Note(title=title, content=content)
        # Añade la nota a la sesión de la base de datos
        db.session.add(note_db)
        # Confirma la transacción con commit()
        db.session.commit()
        # Redirige al usuario a la página principal
        return redirect(url_for('home'))
    
    return render_template('note_form.html')


# Crear una nueva ruta que acepte el ID de la nota como parámetro.
@app.route('/editar-nota/<int:id>', methods=["GET", "POST"])
def edit_note(id):
    # Recuperar la información existente de la base de datos.
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        # actualiza la información de la nota
        note.title = title
        note.content = content
        # Procesar los cambios y actualizarlos en la base de datos.
        db.session.commit()
        return redirect(url_for("home"))
    
    # Mostrar esa información en un formulario para su edición.
    return render_template("edit_note.html", note=note)
    

# Utilizamos solo el método POST para mayor seguridad
@app.route('/eliminar-nota/<int:id>', methods=["POST"])
def delete_note(id):
    # Verificamos que la nota exista antes de intentar eliminarla
    note = Note.query.get_or_404(id)
    # Usamos db.session.delete() pasando la instancia del modelo
    db.session.delete(note)
    # Confirmamos los cambios con commit()
    db.session.commit()
    # Redirigimos al usuario a la página principal
    return redirect(url_for("home"))
    