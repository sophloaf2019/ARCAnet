from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .. import form_to_dict
from ..models import User

import os
import yaml
import markdown
import re

clearance_order = {
    'declassified': 0,
    'sensitive': 1,
    'confidential': 2,
    'classified': 3,
    'secret': 4,
    'top secret': 5,
}

class Entry:
    def __init__(self, name, body, clearance, id):
        self.name = name
        self.body = body
        self.clearance = clearance
        self.id = id

def replace_tags_with_black_box(text, clearance):
    # Define the ASCII black box characte

    # Regular expression pattern to match <clearance: Value></clearance> tags
    pattern = r'<([^>]*)>([^<]*)</\1>'

    # Function to replace the content of the tags with black boxes and remove the tags
    def replace_match(match):
        # Extract the tag type and content
        value = match.group(1).strip()  # e.g., "clearance"
        content = match.group(2).strip()  # e.g., "Content"
        # Replace all non-space characters in the content with the black box character
        black_box = '█'
            
        replaced_content = re.sub(r'[^.,!?\'"(){}\[\]:;\\/\-\s]', black_box, content) if clearance_order[value] > clearance_order[clearance.lower()] else content
        # Construct the new tag with replaced content
        return replaced_content

    # Use re.sub with the pattern and replacement function
    result = re.sub(pattern, replace_match, text)
    return result

def read_markdown_content(file_path):
    """Reads a Markdown file, extracts its content and YAML front matter, and returns an Entry object."""
    if not os.path.isfile(file_path):
        return None

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        if content.startswith('---'):
            _, frontmatter, body = content.split('---', 2)
            yaml_data = yaml.safe_load(frontmatter)
        else:
            body = content
            yaml_data = {}
        body = replace_tags_with_black_box(body, current_user.clearance)
        clearance = yaml_data.get('clearance', 'default_clearance')
        id = yaml_data.get('id', 'default_id')

        # Convert Markdown body to HTML
        body_html = markdown.markdown(body)

        # Create and return an Entry instance
        name = os.path.splitext(os.path.basename(file_path))[0]  # Extract filename without extension
        return Entry(name=name, body=body_html, clearance=clearance, id = id)

def read_all_markdown_files(directory):
    """Reads all Markdown files in the specified directory and returns a list of Entry objects."""
    entries = []

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            entry = read_markdown_content(file_path)
            if entry:
                entries.append(entry)

    return entries

def read_markdown_file(entry_id):
    """Reads a specific Markdown file by entry ID and returns an Entry object."""
    # Calculate the relative path to the dcii_entries directory
    current_dir = os.path.dirname(__file__)
    entries_dir = os.path.join(current_dir, '..', 'dcii_entries')
    entries_dir = os.path.normpath(entries_dir)

    # Construct the expected filename
    filename = f"ENTRY {entry_id}.md"
    file_path = os.path.join(entries_dir, filename)

    return read_markdown_content(file_path)




@app.route('/dcii')
@login_required
def dcii_entries_overview():
    current_dir = os.path.dirname(__file__)  # Directory of the current script
    entries_dir = os.path.join(current_dir, '..', 'dcii_entries')  # Adjust for relative path

    # Normalize the path to handle ".." and other irregularities
    entries_dir = os.path.normpath(entries_dir)

    # Use the function to process the markdown files
    entries = read_all_markdown_files(entries_dir)
    return render_template('dcii_overview.html', entries = entries)

@app.route('/dcii/<int:entry_id>')
def show_entry(entry_id):
    # Read the markdown file and convert it to an Entry object
    entry = read_markdown_file(entry_id)

    # If the file does not exist, return a 404 error
    if entry is None:
        flash('That entry doesn\'t exist.')
        return redirect(url_for('dcii_entries_overview'))
    
    return render_template('show_entry.html', entry = entry)