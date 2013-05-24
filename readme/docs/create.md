# New project 
*Get the `client_secrets.json` file if you don't have it already. Use the `fab newproject` command to kick off a new project by copying a basic
project structure and setting up a Google spreadsheet.*

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

## Automatically creating Google Spreadsheets

*Automatic spreadsheet creation is currently broken.* See [ticket #20](https://github.com/newsapps/tarbell-template/issues/20) for more details and to help troubleshoot this tricky problem. 

<div style="color: #666; font-style: italic;">
In order to allow Tarbell to create new Google Spreadsheets, you'll need to download a <a href="https://developers.google.com/api-client-library/python/guide/aaa_client_secrets">client_secrets.json file</a> from Google to allow access to Drive.

First, log in to the <a href="https://code.google.com/apis/console/b/0/">Google API Developer Console</a> and either create a new project or, if one already exists, click on the API Access tab.

If you don't already have one, create an OAuth 2.0 client ID, and select Web Application as the type. Once the ID has been created, click Download JSON to save the <code>client_secrets.json</code> file to your local machine, and put the file in the root directory of your Tarbell installation.

The <code>fab newproject</code> command detailed below will prompt you if the <code>client_secrets.json</code> file doesn't exist. 
</div>


