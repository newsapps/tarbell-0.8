# New project 
*Get the `client_secrets.json` file if you don't have it already. Use the `fab newproject` command to kick off a new project by copying a basic
project structure and setting up a Google spreadsheet.*

## Prerequisite: Authenticating with Google with client_secrets.json

Tarbell uses the Google Drive API to create new spreadsheets, which
requires going through a little OAuth2 song-and-dance. This is optional but
highly recommended, in part because Tarbell will probably use this technique for
all authentication and access in the future. If you want to skip this step and configure your spreadsheet manually, see
[Manually creating Google spreadsheets](#manual-create).

You ready? Let's go. 

In order to allow Tarbell to create new Google Spreadsheets, you'll need to 
download a <a href="https://developers.google.com/api-client-library/python/guide/aaa_client_secrets">client_secrets.json 
file</a> file to access the Google Drive API. You can share this file with collaborators
and within your organization, but do _not_ share this file anywhere public.

Log in to the <a href="https://code.google.com/apis/console/">Google API Developer Console</a>
and create a new project:

<img src="/readme/img/oauth-01-create-app.png" alt="Create client screenshot" class="doc-img" />

Now click the "Services" tab and enable Google Drive API.

<img src="/readme/img/oauth-02-enable-drive-api.png" alt="Enable Drive API" class="doc-img" />

Click the "API Access" tab to create a client ID:

<img src="/readme/img/oauth-03-create-client-id.png" alt="Create client ID" class="doc-img" />

Add some project details. These don't really matter:

<img src="/readme/img/oauth-04-client-id-screen-1.png" alt="Client ID details screen" class="doc-img" />

This is the important screen. Select "installed app" and "other":

<img src="/readme/img/oauth-04-client-id-screen-2.png" alt="Create ID important screen" class="doc-img" />

Whew! Now you can download the `client_secrets.json` file:

<img src="/readme/img/oauth-05-download-client_secrets.png" alt="Download client_secrets.json" class="doc-img" />

Now put the file in the root directory of your Tarbell installation.

The first time you run <code>fab newproject</code> and answer yes to create a Google spreadsheet, your
default browser will open and you will be prompted to grant your Tarbell client access to your API key. 

<img src="/readme/img/oauth-06-grant-client-access.png" alt="Grant client access" class="doc-img" />

**The first time you create a new project and spreadsheet, make sure you are not running any services on port 8080, such as MAMP.** The Python Google API client library fires up a tiny server on port 8080 to receive and store an access token.

The <code>fab newproject</code> command will prompt you if the <code>client_secrets.json</code> file doesn't exist.

**Help us improve!** We know this step is a little rocky. We'd like to make it
smoother. If you are an OAuth or Google Drive API expert, we need your help. 
See [#21 Improve OAuth workflow for newproject command](https://github.com/newsapps/tarbell-template/issues/21) 
and [#22 Use Drive API in Tarbell library](https://github.com/newsapps/tarbell-template/issues/22).

## Create a project

To create your first project, use the handy `fab` command:

<pre>fab newproject</pre>

You'll be prompted with a series of questions. Here's what you'll see, with user
input <span class="highlight">highlighted</span>.

<pre>What is the directory name for the project? <span class="highlight">newproject</span>
What is your project's full title? <span class="highlight">My New Project</span>
Do you want a Google doc associated with this project? [Y/n]: <span class="highlight">y</span>
Generating Google spreadsheet
Success! View the file at https://docs.google.com/spreadsheet/ccc?key=0Ak3IIavLYTovdFVNSVkxa0M3Tm4xcHpnSUR0Z1NwOUE
...
Would you like to create a new branch and initial commit for this project? [Y/n]: y
[localhost] local: git checkout master; git checkout -b newproject
...
Switched to a new branch 'newproject'
[localhost] local: git add newproject
[localhost] local: git commit -m "Started new project newproject"
[newproject 7dbdb97] Started new project newproject
 3 files changed, 63 insertions(+), 0 deletions(-)
 create mode 100644 newproject/config.py
 create mode 100644 newproject/static/style.css
 create mode 100644 newproject/templates/index.html

Welcome to My New Project. Great work! What's next?

- Edit newproject/config.py to set up default values and Google Doc settings.
- Edit newproject/templates/index.html to edit your default, root template.
- Run `fab runserver` and view your project at http://fab.localhost:5000/newproject/

Run `fab deploy` and `fab project:projectname deploy` to deploy to S3 if you have a bucket configured.

Done.
</pre>

<div id="manual-create"></div>

## Manually creating Google Spreadsheets

To manually set up a Google spreadsheet for your project:

* Create a new Google spreadsheet
* Rename "Sheet1" to "values"
* Add 'key' and 'value' column headers in the first row
* Add the spreadsheet key in `projectname/config.py`
* Public access:
  * Set the spreadsheet to 'publish to the web'
* Private access:
  * Grant access to a special user account (you'll be storing password in the clear, so set up a new account for this) 
  * Add credentials to `projectname/secrets.py`
