from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .. import form_to_dict
from ..models import User

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = form_to_dict(request.form)
        try:
            user = User.query.filter_by(username = data.get('username')).one()
        except:
            user = None
        if not user:
            flash('That username doesn\'t exist.')
            return redirect(url_for('login'))
        if user and user.password == data.get('password'):
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            flash('Incorrect password.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))