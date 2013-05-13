# Deploy
*Use `fab deploy` and `fab project:<projectname> deploy` to upload your project to Amazon S3. Customize the publishing process.*

## Amazon S3 setup

An Amazon S3 publishing workflow is included in the Tarbell template. To use it, you'll need your [Amazon S3 credentials](https://portal.aws.amazon.com/gp/aws/developer/account/index.html?action=access-key). 

Create a file called `s3config.py` in your Tarbell template directory.

<pre><code class="python">S3CONFIG = {
    'bucket': 'mybucket.domain.com',
    'key': 'KEY',
    'key_id': 'KEYID',
}
</code></pre>

## Deploying

Once your Amazon S3 access credentials are configured, deploying all projects
is very simple:

<pre>fab deploy</pre>

You should see something like:

<pre>
[localhost] local: python render_templates.py 
Rendering templates.

Generating project 'base' in /Users/davideads/Repos/tarbell-template/out/
-- No Google doc configured for base.

Generating project 'readme' in /Users/davideads/Repos/tarbell-template/out/readme
-- Created JSON /Users/davideads/Repos/tarbell-template/out/readme/json/values.json
-- Created JSON /Users/davideads/Repos/tarbell-template/out/readme/json/LAST_UPDATED.json
-- Created JSON /Users/davideads/Repos/tarbell-template/out/readme/json/projects.json
-- Created page /Users/davideads/Repos/tarbell-template/out/readme/index.html

[localhost] local: python s3deploy.py
Deploying to tarbell.recoveredfactory.net
Uploading css/style.css
Uploading js/app.js
Uploading js/templates/nav.jst
Uploading js/views/NavigationView.js
Uploading readme/index.html
Refreshing Facebook info for: http://tarbell.recoveredfactory.net/readme/index.html?fbrefresh=CANBEANYTHING
Uploading readme/bootstrap/css/bootstrap.css
Uploading readme/bootstrap/css/bootstrap.min.css
Uploading readme/bootstrap/img/glyphicons-halflings-white.png
Uploading readme/bootstrap/img/glyphicons-halflings.png
Uploading readme/bootstrap/js/bootstrap.js
Uploading readme/bootstrap/js/bootstrap.min.js
Uploading readme/css/ir_black.css
Uploading readme/css/style.css
Uploading readme/img/google-screenshot.jpg
Uploading readme/img/html-edit-screenshot.jpg
Uploading readme/img/ida-tarbell.jpg
Uploading readme/img/s3-publish-screenshot.jpg
Uploading readme/js/app.js
Uploading readme/json/LAST_UPDATED.json
Uploading readme/json/projects.json
Uploading readme/json/values.json
</pre>

To deploy a specific project, use the `project:PROJECTNAME` flag:

<pre>fab project:PROJECTNAME deploy</pre>

**Please note**: The base template is always published -- it is assumed most
projects will use some base components.
