import imp
import os
import StringIO

"""
Google doc configuration. If not provided, no Google doc will be used.

See secrets.py to configure access.
"""

GOOGLE_DOC = {
    'key': '0Ak3IIavLYTovdGRrdjBwbS1Gd3R4TEZoQXQtQk1fMnc',
}

"""
Set default context. These variables will be globally available to the template.
"""
DEFAULT_CONTEXT = {
    'title': 'Tarbell Readme',
}

"""
Root URL project will appear at (e.g. http://mydomain.tld/)
"""
# URL_ROOT = 'readme'

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
from flask import Blueprint
blueprint = Blueprint('readme', __name__)

def get_doc(file):
    path = os.path.join(os.path.dirname(__file__), 'docs', '%s.md' % file)
    return open(path, 'r').read()

@blueprint.app_context_processor
def context_processor():
    """ Readme context processor. Get docs from docs dir."""
    sections = [
        { 'id': 'install', 'navtitle': 'Install Tarbell', 'body': get_doc('install') },
        { 'id': 'build', 'navtitle': 'Create project', 'body': get_doc('start') },
        { 'id': 'build', 'navtitle': 'Build project', 'body': get_doc('build') },
        { 'id': 'deploy', 'navtitle': 'Deploy project', 'body': get_doc('deploy') },
    ]
    return { 'sections': sections }


"""
Load secrets. This is goofy but it works, and `import secrets` sadly doesn't.

Don't change this unless you know what you're doing.
"""
def get_secrets():
    """ Return a secrets module """
    root = os.path.dirname(os.path.abspath(__file__))
    return imp.find_module('secrets', [root])

secrets = imp.load_module('secrets', *get_secrets())

if hasattr(secrets, 'GOOGLE_AUTH'):
    GOOGLE_DOC.update(secrets.GOOGLE_AUTH)


