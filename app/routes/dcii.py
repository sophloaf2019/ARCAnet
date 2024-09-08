import re
import markdown
from termcolor import cprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import db, form_to_dict
from ..models import DCIIAddon, DCIIEntry, DCIISubject, User

clearance_order = {
    'declassified': 0,
    'sensitive': 1,
    'confidential': 2,
    'classified': 3,
    'secret': 4,
    'top secret': 5,
}

def process_tags(input_string, current_user):
    # Regular expression pattern to find tags in the format <number>Data</number>
    pattern = r'<(\d+)>([^<]+)</\1>'

    def redact_content(tag_number, tag_content):
        if current_user.clearance < tag_number:
            # Replace alphanumerical characters with vertical black box
            return re.sub(r'[a-zA-Z0-9]', '█', tag_content)
        else:
            return tag_content

    def apply_redaction(match):
        tag_number = int(match.group(1))
        tag_content = match.group(2)
        redacted_content = redact_content(tag_number, tag_content)
        return f'{redacted_content}'

    # Process the input string from innermost to outermost tags
    while re.search(pattern, input_string):
        result = re.sub(pattern, apply_redaction, input_string)
        input_string = result

    return input_string
        
        
@app.template_filter('process_tags')
def process_tags_filter(input_string, mass_clearance, current_user):
    input_string = str(input_string)
    input_string = "<" + str(mass_clearance) + ">" + input_string + "</" + str(mass_clearance) + ">"
    return process_tags(str(input_string), current_user)

@app.template_filter('markdown_render')
def markdown_render(input_string):
    return markdown.markdown(input_string)

@app.route('/dcii')
@login_required
def dcii_entries_overview():
    entries = DCIIEntry.query.all()
    return render_template('dcii/dcii_overview.html', entries = entries)

@app.route('/dcii/<int:entry_id>')
@login_required
def show_entry(entry_id):
    entry = DCIIEntry.query.get(entry_id)
    return render_template('dcii/show_entry.html', entry = entry)

@app.route('/dcii/add_new_entry', methods=['GET', 'POST'])
@login_required
def add_new_entry():
    if request.method == "POST":
        data = form_to_dict(request.form)
        new_entry = DCIIEntry(id = data.get('id'))
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('add_new_entry'))
    if current_user.clearance >= 4:
        entries = DCIIEntry.query.all()
        return render_template('dcii/add_new_entry.html', entries = entries)
    else:
        flash('You can\'t access that page.')
        return redirect(url_for('dcii_entries_overview'))
    
@app.route('/dcii/<int:id>/add_new_subject', methods=['GET', 'POST'])
@login_required
def add_new_subject(id):
    if current_user.clearance >= 4:
        if request.method == "POST":
            data = form_to_dict(request.form)
            new_subject = DCIISubject()
            for key, value in data.items():
                if hasattr(new_subject, key):  # Check if the instance has the attribute
                    setattr(new_subject, key, value)  # Set the attribute value
            new_subject.entry_id = id
            db.session.add(new_subject)
            db.session.commit()
            return redirect(url_for('add_new_subject', id = id))
        entry = DCIIEntry.query.get(id)
        if entry:
            return render_template('dcii/add_new_subject.html', entry = entry)
        else:
            flash('That entry has been deleted.')
            return redirect(url_for('dcii_entries_overview'))
    else:
        flash('You can\'t access that page.')
        return redirect(url_for('dcii_entries_overview'))

@app.route('/dcii/<int:entry_id>/<int:subject_id>/add_addons', methods=['GET','POST'])
@login_required
def add_addons(entry_id, subject_id):
    if current_user.clearance >= 4:
        if request.method == "POST":
            data = form_to_dict(request.form)
            new_addon = DCIIAddon()
            for key, value in data.items():
                if hasattr(new_addon, key):  # Check if the instance has the attribute
                    setattr(new_addon, key, value)  # Set the attribute value
            new_addon.subject_id = subject_id
            db.session.add(new_addon)
            db.session.commit()
            return redirect(url_for('add_addons', entry_id = entry_id, subject_id = subject_id))
        entry = DCIIEntry.query.get(entry_id)
        subject = DCIISubject.query.filter_by(entry_id=entry.id, index=subject_id).first()
        print(entry_id)
        print(subject_id)
        if entry and subject:
            return render_template("dcii/add_new_addons.html", entry = entry, subject = subject)
        else:
            flash('That entry has been deleted.')
            return redirect(url_for('dcii_entries_overview'))
    else:
        flash('You can\'t access that page.')
        return redirect(url_for('dcii_entries_overview'))
    
    
@app.route('/dcii/<int:id>/edit', methods = ['GET','POST'])
@login_required
def edit_entry(id):
    entry = DCIIEntry.query.get(id)
    if request.method == "POST":
        data = form_to_dict(request.form)
        try:
            for key, value in data.items():
                if hasattr(entry, key):  # Check if the instance has the attribute
                    setattr(entry, key, value)  # Set the attribute value
        
            db.session.commit()
            flash("Changes saved.")
            return redirect(url_for('edit_entry', id = entry.id))
        except Exception as e:
            flash(str(e))
        
    return render_template('dcii/edit_entry.html', entry = entry)

@app.route('/dcii/<int:entry_id>/<int:subject_id>/edit', methods = ['GET','POST'])
@login_required
def edit_subject(entry_id, subject_id):
    subject = DCIISubject.query.filter_by(entry_id=entry_id, index=subject_id).first()
    if request.method == "POST":
        data = form_to_dict(request.form)
        try:
            for key, value in data.items():
                if hasattr(subject, key):  # Check if the instance has the attribute
                    setattr(subject, key, value)  # Set the attribute value
        
            db.session.commit()
            flash("Changes saved.")
            return redirect(url_for('edit_subject', entry_id = subject.entry.id, subject_id = subject.index))
        except Exception as e:
            flash(str(e))
        
    return render_template('dcii/edit_subject.html', subject = subject)

@app.route('/dcii/<int:entry_id>/<int:subject_id>/<int:addon_id>/edit', methods = ['GET','POST'])
@login_required
def edit_addon(entry_id, subject_id, addon_id):
    entry = DCIIEntry.query.get(entry_id)
    if entry:
        subject = next((s for s in entry.subjects if s.index == subject_id), None)
        if subject:
            addon = next((a for a in subject.addons if a.index == addon_id), None)
            if addon:
                if request.method == "POST":
                    data = form_to_dict(request.form)
                    try:
                        for key, value in data.items():
                            if hasattr(addon, key):  # Check if the instance has the attribute
                                setattr(addon, key, value)  # Set the attribute value
                    
                        db.session.commit()
                        flash("Changes saved.")
                        return redirect(url_for('edit_addon', entry_id = addon.subject.entry.id, subject_id = addon.subject.index, addon_id = addon.index))
                    except Exception as e:
                        flash(str(e))
                return render_template('dcii/edit_addon.html', addon = addon)