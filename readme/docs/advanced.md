# Advanced
*Configure Tarbell, set up a Flask Blueprint, and edit the default Javascript app.*

## Configuring Tarbell

When your project was created, a <code>config.py</code> file was created in 
the project directory, which lets Tarbell find your project. This file can be 
empty, but also accepts several configuration options:</p>

<ul>
    <li>
        <p><code>GOOGLE_DOC</code>: A dict of Google docs parameters
            to access a spreadsheet. Takes <code>key</code>,
            <code>account</code>, and <code>password</code> parameters.</p>

        <p>The default template stores account and password variables in a file
           called `secrets.py` in variable called `GOOGLE_AUTH`. <strong>Use
           secrets.py to keep your authentication information out of version
           control.</strong></p>

<pre><code class="python">GOOGLE_DOC = {
    'key': "BIGLONGSTRINGOFLETTERSANDNUMBERS",
    'account': "some+account@gmail.com",
    'password': "++GmailPassWord++",
}</code></pre>
    </li>
    <li><p><code>DEFAULT_CONTEXT</code>: Default context
    variables to make available to all project templates.</p>
<pre><code class="python">DEFAULT_CONTEXT = {
    'ad_path': '',
    'analytics_path': '',
}</code></pre>
    </li>
    <li><p><code>DONT_PUBLISH</code>: If <code>True</code>, this
    project will not be published to S3.</p>
    <pre>DONT_PUBLISH=True</pre>
    <p>Default: <code>False</code></p>
    </li>
    <li><p><code>URL_ROOT</code>: Override the published URL to
    differ from the directory name.</p> 
    <pre>URL_ROOT='totally-awesome-project'</pre>
    <p>Default: <code>None</code> (publish using name of directory)</p>
    </li>
    <li><p><code>CREATE_JSON</code>: If <code>False</code>, do not publish
    JSON data. Useful if spreadsheets contain secrets or sensitive information, and so should not be public.</p>
    <pre>CREATE_JSON = False</pre>
    <p>Default: <code>True</code></p></li>
</ul>

<p>For advanced uses, you can turn your project into a Flask Blueprint in order to
register template filters or special URLS.</p>

<pre><code class="python">from flask import Blueprint
blueprint = Blueprint('awesome_project', __name__)

# Register template filter
@blueprint.app_template_filter('example_filter')
def example_filter(text):
   return text.strip()

# Will be available at URL_ROOT/test
@blueprint.route('/test')
def test_route():
   return render_template('awesome_project/test.html', context_var='test')</code></pre>

