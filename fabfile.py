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
import s3config


"""
Base configuration
"""
fab.env.oauth_scope = 'https://www.googleapis.com/auth/drive.file'
fab.env.oauth_redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
fab.env.project = ''

def project(project=None):
    """
    Set project
    """
    if project:
        fab.env.project = project


def deploy():
    """
    Deploy from fab.locally rendered files.
    """
    fab.local('python render_templates.py %(project)s' % fab.env)
    fab.local('python s3deploy.py')


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
    with fab.lcd('out'):
        fab.local('python -m SimpleHTTPServer 5001')


def newproject(project_name=None):
    """Create new project in the current directory."""
    FLAGS = gflags.FLAGS
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

    try:
        os.mkdir(proj_dir)
    except OSError, e:
        if e.errno == 17:
            print ("ABORTING: Directory %s "
                   "already exists.") % context['project_name']
        else:
            print "ABORTING: OSError %s" % e
        return

    # if client secrets exists
    setup_google = raw_input("Do you want a Google doc associated with this "
                             "project? [Y/n]: ")
    if setup_google.lower() == 'y':
        print "Generating Google spreadsheet"
        context['spreadsheet_key'] = _create_google_spreadsheet(
            context['long_name'])

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
    print ("- Run `fab runserver` and view your project at "
           "http://localhost:5000/%s/") % context['project_name']
    print
    print ("Run `fab deploy` and `fab project:projectname deploy` to deploy to "
           "S3 if you have a bucket configured.")


def _handle_oauth_flow(storage):
    """
    Reads the fab.local client secrets file if available (otherwise, opens a
    browser tab to walk through the OAuth 2.0 process, and stores the client
    secrets for future use) and then authorizes those credentials. Returns an
    httplib2.Http object authorized with the fab.local user's credentials.
    """
    # Retrieve credentials from fab.local storage, if possible
    credentials = storage.get()
    if not credentials:
        flow = client.flow_from_clientsecrets('client_secrets.json',
            scope=fab.env.oauth_scope, redirect_uri=fab.env.oauth_redirect_uri)
        credentials = tools.run(flow, storage)
        storage.put(credentials)
    http = httplib2.Http()
    http = credentials.authorize(http)
    return http


def _add_user_to_file(file_id, service, user_email='tribgfx@gmail.com',
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


def _create_google_spreadsheet(project_name):
    """
    Once credentials are received, uploads a copy of microcopy_template.xlsx
    named for this project, puts it in the Trib Docs -> microcopy folder, adds
    the default tribapps gmail account as a reader, makes it world-readable and
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
        _add_user_to_file(newfile['id'], service)
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
