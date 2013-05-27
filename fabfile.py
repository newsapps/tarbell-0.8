# Tarbell template fabfile
from fabric import api as fab
import os
import jinja2
import codecs
from tarbell.app import TarbellSite as _TarbellSite
import inspect
from apiclient import errors
from apiclient import discovery
from apiclient.http import MediaFileUpload as _MediaFileUpload
from oauth2client import client
from oauth2client import keyring_storage
from oauth2client import tools
import getpass
import gflags
import httplib2

FLAGS = gflags.FLAGS

"""
Base configuration
"""
fab.env.oauth_scope = 'https://www.googleapis.com/auth/drive.file'
fab.env.oauth_redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
fab.env.target = 'production'
fab.env.project = ''


def project(project=None):
    """
    Set project (default: none).
    """
    if project:
        fab.env.project = project


def target(target):
    """
    Set target (default: production).
    """
    fab.env.target = target


def deploy():
    """
    Deploy from fab.locally rendered files.
    """
    fab.local('python render_templates.py %(project)s' % fab.env)
    fab.local('python s3deploy.py -b %(target)s' % fab.env)


def runserver():
    """Run a fab.local development server."""
    print "Point your browser to http://localhost:5000/"
    print "Type ctrl-c to quit."
    fab.local('python runserver.py' % fab.env)


def runpreviewserver():
    """Render static HTML and preview with a simple HTTP server."""
    fab.local('python render_templates.py %(project)s' % fab.env)
    print "Point your browser to http://localhost:5001/<projectname>/"
    print "Type ctrl-c to quit."
    with fab.lcd('_out'):
        fab.local('python -m SimpleHTTPServer 5001')


def newproject(project_name=None):
    """Create new project in the current directory."""
    context = {}

    if project_name is None:
        context['project_name'] = raw_input(
            "What is the directory name for the project? ")
    else:
        context['project_name'] = project_name

    context['long_name'] = context['project_name']
    long_name = raw_input("What is your project's full title? ")
    if long_name:
        context['long_name'] = long_name

    proj_dir = os.path.join(os.path.dirname(__file__), context['project_name'])

    # Encapsulates Google spreadsheet setup
    context = _setup_google_spreadsheet(context)

    try:
        os.mkdir(proj_dir)
    except OSError, e:
        if e.errno == 17:
            print ("ABORTING: Directory %s "
                   "already exists.") % context['project_name']
        else:
            print "ABORTING: OSError %s" % e
        return

    # Get and walk project template
    loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '_project_template'))
    fab.env = jinja2.Environment(loader=loader)

    for template in loader.list_templates():
        if template.endswith('.xlsx'):
            continue

        if ('/') in template:
            parts = template.split('/')
            dirname = '/'.join(parts[:-1])
            new_dir = os.path.join(proj_dir, dirname)
            try:
                os.makedirs(new_dir)
                print "Created directory %s" % new_dir
            except OSError, e:
                if e.errno != 17:
                    print "Error creating %s: %s" % (new_dir, os.strerror)

        content = fab.env.get_template(template).render(**context)
        new_file = os.path.join(proj_dir, template)
        codecs.open(new_file,"w",encoding="utf-8").write(content)
        print 'Created %s' % new_file

    if os.path.isdir(os.path.join(os.path.dirname(__file__), '.git')):
        branch = raw_input("Would you like to create a new branch and initial "
                           "commit for this project? [Y/n]: ")
        if branch.lower() == 'y':
            try:
                fab.local('git checkout master; \
                    git checkout -b %s' % context['project_name'] )
                fab.local('git add %s' % context['project_name'])
                fab.local('git commit -m "Started new project \
                    %s"' % context['project_name'])
            except:
                print "Error checking out branch."
        else:
            print "Okay! No new branch..."

    print
    print "Welcome to %s. Great work! What's next?" % context['long_name']
    print
    print ("- Edit %s to set up template values and adjust project "
           "settings.") % os.path.relpath(os.path.join(proj_dir, 'config.py'))
    print ("- Edit %s to configure Google spreadsheet authentication "
           "variables.") % os.path.relpath(os.path.join(proj_dir, 'secrets.py'))
    print "- Edit %s to edit your default template." %\
        os.path.relpath(os.path.join(proj_dir, 'templates/index.html'))
    print "- Edit %s to edit your default Javascript app." %\
        os.path.relpath(os.path.join(proj_dir, 'static/js/app.js'))
    print ("- Run `python runserver.py` and view your project at "
           "http://localhost:5000/%s/") % context['project_name']
    print
    print ("Run `fab deploy` and `fab project:projectname deploy` to deploy to "
           "S3 if you have a bucket configured.")


def _setup_google_spreadsheet(context):
    try:
        with open('client_secrets.json'):
            setup_google = raw_input("Do you want a Google doc associated with "
                                     "this project? [Y/n]: ")
            if setup_google.lower() != 'n':
                print "Generating Google spreadsheet"
                email = raw_input("What gmail account should have access to this spreadsheet? (e.g. foo@gmail.com) ")
                context['spreadsheet_key'] = _create_google_spreadsheet(
                    context['long_name'], email)
            return context
    except IOError:
        print ""
        print ("You don't have the `client_secrets.json` file required to "
               "create Google spreadsheets using the Drive API.")
        print ""
        print "First, log in to the [Google API Developer Console](https://code.google.com/apis/console/)"
        print "and click \"Create project\". After creating a project (or if one" 
        print "already exists), click on the API Access tab."
        print ""
        print "If you don't already have one, create an OAuth 2.0 client ID, "
        print "and select Web Application as the type. Once the ID has been"
        print "created, click Download JSON to save the `client_secrets.json` file"
        print "to your local machine, and put the file in the root directory of your "
        print "Tarbell installation."
        print ""
        print "There's no problem if you want to skip this step, you'll just have to"
        print "manage template variables or manually configure spreadsheet access in"
        print "your new project's `config.py`."
        print ""
        retry = raw_input("Want to try again? [y/N]: ")
        if retry.lower() == 'y':
            return _setup_google_spreadsheet(context)
        else:
            print "No Google spreadsheet configured."
        return context

def _handle_oauth_flow(storage):
    """
    Reads the fab.local client secrets file if available (otherwise, opens a
    browser tab to walk through the OAuth 2.0 process, and stores the client
    secrets for future use) and then authorizes those credentials. Returns an
    httplib2.Http object authorized with the fab.local user's credentials.
    """
    # Retrieve credentials from local storage, if possible
    credentials = storage.get()
    if not credentials:
        flow = client.flow_from_clientsecrets('client_secrets.json', scope=fab.env.oauth_scope)
        credentials = tools.run(flow, storage)
        storage.put(credentials)
    http = httplib2.Http()
    http = credentials.authorize(http)
    return http


def _add_user_to_file(file_id, service, user_email,
                        perm_type='user', role='reader'):
    """
    Grants the given set of permissions for a given file_id. service is an
    already-credentialed Google Drive service instance.
    """
    new_permission = {
        'value': user_email,
        'type': perm_type,
        'role': role
    }
    try:
        service.permissions()\
            .insert(fileId=file_id, body=new_permission)\
            .execute()
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def _create_google_spreadsheet(project_name, email):
    """
    Once credentials are received, uploads a copy of microcopy_template.xlsx
    named for this project, makes it world-readable and
    returns the file ID.
    """
    storage = keyring_storage.Storage('fab', getpass.getuser())
    http = _handle_oauth_flow(storage)
    service = discovery.build('drive', 'v2', http=http)
    path = os.path.join(os.path.dirname(inspect.getfile(_TarbellSite)),
                        'project_template/microcopy_template.xlsx')
    media_body = _MediaFileUpload(path, mimetype='application/vnd.ms-excel')
    body = {
        'title': '%s microcopy' % project_name,
        'description': 'Microcopy file for %s project' % project_name,
        'mimeType': 'application/vnd.ms-excel',
    }
    try:
        newfile = service.files()\
            .insert(body=body, media_body=media_body, convert=True).execute()
        _add_user_to_file(newfile['id'], service, user_email=email)
        _add_user_to_file(newfile['id'], service, user_email='anyone',
                          perm_type='anyone', role='reader')
        service.revisions()\
            .update(fileId=newfile['id'], revisionId='head',
                    body={'published': True, 'publishAuto': True}).execute()
        print ("Success! View the file at "
               "https://docs.google.com/spreadsheet/ccc?key=%s") % newfile['id']
        return newfile['id']
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        return '<< INSERT SPREADSHEET KEY >>'
