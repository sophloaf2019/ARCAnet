from flask import current_app as app
"""

the routes package

observe yourresource.py for a template.

ensure that all resources are imported into this package.

"""

from .home import *
from .dcii import *

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

# ENABLE THIS IF YOU WANT TO DISALLOW PAGE CACHING
# 
# @app.after_request
# def add_cache_control(response):
#     # Prevent caching of sensitive pages
#     response.cache_control.no_store = True
#     response.cache_control.no_cache = True
#     response.cache_control.must_revalidate = True
#     return response