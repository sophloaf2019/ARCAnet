from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import db, form_to_dict
from ..models import User

@app.route('/admin')
@login_required
def user_profiles():
    users = User.query.all()
    return render_template('admin/users.html', users = users)

@app.route('/admin/<username>')
@login_required
def open_user_profile(username):
    user = User.query.filter_by(username = username).first()
    return render_template('admin/show_user.html', user = user)

@app.route('/admin/<username>/edit_profile')
@login_required
def edit_profile(username):
    user = User.query.filter_by(username = username).first()
    if current_user.clearance >= 4 or user == current_user:  
        return render_template('admin/edit_profile.html', user = user)
    else:
        flash("You can't access that page.")
        return redirect(url_for('user_profiles'))

@app.route('/admin/<username>/save_profile', methods = ['GET', 'POST'])
@login_required
def save_profile(username):
    user = User.query.filter_by(username = username).first()
    if current_user.clearance >= 4 or user == current_user:
        data = form_to_dict(request.form)
        for key, value in data.items():
            if hasattr(user, key):  # Check if the instance has the attribute
                setattr(user, key, value)  # Set the attribute value
        db.session.commit()
        flash('Changes saved.')
        return render_template('admin/edit_profile.html', user = user)