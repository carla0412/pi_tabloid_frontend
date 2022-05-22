from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user 
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note está muito curto', category='error')
        else:
            new_note = Note(data = note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note adicionado', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/admin')
@login_required
def admin():
    return render_template("admin.html", user=current_user)

@views.route('/teste')
def teste():
    return render_template("teste.html", user=current_user)
    
@views.route('/mercadob')
def mercadob():
    return render_template("mercadob.html", user=current_user)

@views.route('/mercadoc')
def mercadoc():
    return render_template("mercadoc.html", user=current_user)