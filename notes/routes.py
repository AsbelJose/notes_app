from flask import ( 
    request,  
    render_template, 
    redirect, 
    url_for,
    Blueprint,
    flash,
    session
    )
from models import Note, db

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/")
def home():
    if "user" not in session:
        flash("Para poder ver las notas debes iniciar session", "error")
        return redirect(url_for("auth.login"))
    notes = Note.query.all() # obtiene todas las notas de la base de datos.
    return render_template("home.html", notes=notes )

@notes_bp.route("/crear-nota", methods=["GET", "POST"])
def create_note():

    if request.method == "POST":
        # Obtiene los datos del formulario (título y contenido)
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        # Crea una nueva instancia del modelo Note con esos datos
        
        if not len(title.strip()) > 10:
            flash("El título es muy corto, minimo 10", "error")
            return render_template("note_form.html")
        
        if not len(content.strip()) > 300:
            flash("El título es muy corto, minimo 300", "error")
            return render_template("note_form.html")
        
        
        note_db = Note(title=title, content=content)
        # Añade la nota a la sesión de la base de datos
        db.session.add(note_db)
        # Confirma la transacción con commit()
        db.session.commit()
        # Redirige al usuario a la página principal

        flash("Nota Creada", "Success")
        return redirect(url_for('notes.home'))
    
    return render_template('note_form.html')


# Crear una nueva ruta que acepte el ID de la nota como parámetro.
@notes_bp.route('/editar-nota/<int:id>', methods=["GET", "POST"])
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
    return render_template("notes.edit_note.html", note=note)
    

# Utilizamos solo el método POST para mayor seguridad
@notes_bp.route('/eliminar-nota/<int:id>', methods=["POST"])
def delete_note(id):
    # Verificamos que la nota exista antes de intentar eliminarla
    note = Note.query.get_or_404(id)
    # Usamos db.session.delete() pasando la instancia del modelo
    db.session.delete(note)
    # Confirmamos los cambios con commit()
    db.session.commit()
    # Redirigimos al usuario a la página principal
    return redirect(url_for("notes.home"))
