from flask import current_app as app
"""

the routes package

observe yourresource.py for a template.

ensure that all resources are imported into this package.

"""

from .home import *
from .dcii import *
from .admin import *

# FILTERS
@app.template_filter('comma_format')
def comma_format(value):
    if value is None:
        value = 0
    try:
        value = float(value)
        formatted_value = "{:,.2f}".format(value)
        
        # Remove the decimal part if it's .00
        if formatted_value.endswith('.00'):
            formatted_value = formatted_value[:-3]
        
        return formatted_value
    except Exception as e:
        return e

@app.template_filter('format_phone_number')
def format_phone_number(phone_number):
    if not phone_number.isdigit():
        raise ValueError("Input must be a string of digits")
    
    # Handle phone numbers with at least 10 digits
    if len(phone_number) < 10:
        raise ValueError("Input must be at least 10 digits long")
    
    if len(phone_number) == 10:
        # Format 10-digit phone numbers
        formatted_number = f"({phone_number[:3]}) {phone_number[3:6]} {phone_number[6:]}"
    else:
        # Handle phone numbers with more than 10 digits
        extra_digits = phone_number[:-10]
        formatted_number = f"{extra_digits} ({phone_number[-10:-7]}) {phone_number[-7:-4]} {phone_number[-4:]}"
    
    return formatted_number

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
    return markdown.markdown(str(input_string))

# ENABLE THIS IF YOU WANT TO DISALLOW PAGE CACHING
# 
# @app.after_request
# def add_cache_control(response):
#     # Prevent caching of sensitive pages
#     response.cache_control.no_store = True
#     response.cache_control.no_cache = True
#     response.cache_control.must_revalidate = True
#     return response