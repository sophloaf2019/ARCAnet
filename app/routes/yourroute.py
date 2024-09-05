from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .. import form_to_dict
from ..resources import YourResource

@app.route('/yourroute')
# @login_required
def yourroute(id = None):
    pass

@app.route('/yourroute/save', methods=['POST'])
@login_required
def save_yourmodel():
    data = form_to_dict(request.form)
    success, message, yourmodel = YourResource.update_from_data(data)
    flash(message)
    return redirect(url_for('yourroute'))