# Flask Boilerplate
## Getting started
To get started, create a virtual environment:

```
python -m venv venv
```

Activate your virtual environment:

Windows CMD
```pwsh
venv\Scripts\activate.bat
```

Windows Powershell
```pwsh
venv\Scripts\Activate.ps1
```

MacOS and Linux
```sh
source venv/bin/activate
```

Install the requirements:

```pwsh
python -m pip install -r requirements.txt
```

Activate with this command:
```pwsh
python run.py
```

## Overview
This is a boilerplate consisting of Flask and some helpful addons. The `app` folder contains the entire application, which is launched in `run.py`.

This boilerplate ships with a helpful colored terminal output library for easier debugging.

```py
from termcolor import cprint

cprint("Hello, world!", 'red')
```

This boilerplate also ships with HTMX, a powerful wrapper for AJAX that allows for some great flexibility.

### `app/components`
The `components` folder contains Jinja2 macros that allow you to reuse components easily. Here's a brief example:

```jinja
{# Declare macros in 'buttons.html' #}
{% macro primary_button(label, additional_classes='', button_id='') %}
    <button type="button" class="btn btn-primary {{ additional_classes }}" id="{{ button_id }}">
        {{ label }}
    </button>
{% endmacro %}

{# Use macro in 'templates/test.html' #}
{% import 'components/buttons.html' as buttons %}
{{ buttons.primary_button('Click Me', 'btn-lg', 'my-button') }}
```

### `app/models`
This package stores all the database models your application uses.

A short sample model is included.

### `app/resources`
This package stores resources that interact with the database for you, to keep your `routes` clean. 

This is important for data validation and other checks or advanced queries.

A short sample resource for the prior sample model is included.

### `app/routes`
All of your defined routes. If using a login functionality, use the `@login_required` decorator on the routes that need a login.

A short and non-functional route exists for the sample resource.

### `app/static`
Contains `.css` and `.js` files. Comes with HTMX.

### `app/templates`
Where you store your `.html` templates.

### `app/__init__.py`
The app factory. You'll want to head in to set your login specifics if using Flask-Login.

### `app.db`
Your main database file. Use migrations from Flask-Migrate when you change columns in your `models`.

```pwsh
flask db migrate -m "Added column 'price'"
flask db upgrade
```

### `config.py`
Stores Flask config variables.

### `README.md`
This file.

### `requirements.txt`
The Python packages used in this project.

### `run.py`
Generates the app and serves it.