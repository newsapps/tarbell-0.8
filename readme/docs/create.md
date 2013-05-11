# New project 
*Use the `fab newproject` command to kick off a new project by copying a basic
project structure and setting up a Google spreadsheet.*

## Create a project

To create your first project, use `fab`.

<pre><code class="bash">fab newproject</code></pre>

You'll be prompted with a series of questions. Here's what you'll see, with user
input <span class="highlight">highlighted</span>.

<pre><code class="bash">What is the directory name for the project? <span class="highlight">newproject</span>
What is your project's full title? <span class="hightlight">My New Project</span>
Do you want a Google doc associated with this project? [Y/n]: <span class="hightlight">y</span>
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
</code></pre>

## Project layout

## Editing templates

## Editing Javascript app
