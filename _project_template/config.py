"""
Google doc configuration. If not provided, no Google doc will be used.
"""
{% if spreadsheet_key %}
GOOGLE_DOC = {
    'key': '{{ spreadsheet_key }}',
}
{% else %}
# GOOGLE_DOC = {
#     'key': '<spreadsheet key>',
# }
{% endif %}

"""
Set default context. These variables will be globally available to the template.
"""
DEFAULT_CONTEXT = {
    'title': '{{ long_name }}',
}

"""
Root URL project will appear at (e.g. http://mydomain.tld/{{ url_root }})
"""
# URL_ROOT = '{{ project_name }}'

"""
Don't render to static HTML.
"""
# DONT_PUBLISH = False

"""
Don't create JSON for project (default: true)
"""
# CREATE_JSON = False


"""
Uncomment the following lines to provide this configuration file as a Flask
blueprint.
"""
# from flask import Blueprint
# blueprint = Blueprint('{{ project_name }}', __name__)


"""
Example use of flask blueprint to add a template filter.
"""
# @blueprint.app_template_filter('example_filter')
# def example_filter(text):
#    return text + ' ...suffix.'


"""
Load secrets. Don't change this unless you know what you're doing.
"""
import os
import imp
try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secrets.py')):
        def get_secrets():
            """ Return a secrets module """
            root = os.path.dirname(os.path.abspath(__file__))
            return imp.find_module('secrets', [root])

        secrets = imp.load_module('secrets', *get_secrets())

        if hasattr(secrets, 'GOOGLE_AUTH'):
            GOOGLE_DOC.update(secrets.GOOGLE_AUTH)
except IOError: pass
