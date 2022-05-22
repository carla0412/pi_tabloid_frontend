from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import null
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user 



auth = Blueprint('auth', __name__)

@auth.route('/login',  methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                 flash('Logado com sucesso', category='success')
                 login_user(user, remember=True)
                 return redirect(url_for('views.admin'))
            else:
                flash('Incorreto password, tente novamente!', category='error')
        else:
            flash('Email não existente', category='error')
       
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email deve ser informado', category='error')
        if len(email)< 4:
            flash('email deve ter mais de 4 caracteres', category='error')
        elif len(nome) < 2:
            flash(' nome deve ter mais de um caractere', category='error')
        elif len(password1) < 6:
            flash(' Senha deve ter mais de 6 caractere', category='error')
        elif (password2) != password1:
            flash('Senhas não correspondentes', category='error')
        else:
            # add user to database
            new_user = User(email=email, nome=nome, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('conta criado com sucesso!', category='success')
            return redirect(url_for('views.home'))



    return render_template('sign_up.html', user=current_user)