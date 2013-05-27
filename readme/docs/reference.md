# Reference
*Configure Tarbell, set up a Flask Blueprint, special base project.*

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
    <pre><code class="python">DONT_PUBLISH=True</code></pre>
    <p>Default: <code>False</code></p>
    </li>
    <li><p><code>URL_ROOT</code>: Override the published URL to
    differ from the directory name.</p> 
    <pre><code class="python">URL_ROOT='totally-awesome-project'</code></pre>
    <p>Default: <code>None</code> (publish using name of directory)</p>
    </li>
    <li><p><code>CREATE_JSON</code>: If <code>False</code>, do not publish
    JSON data. Useful if spreadsheets contain secrets or sensitive information, and so should not be public.</p>
    <pre><code class="python">CREATE_JSON = False</code></pre>
    <p>Default: <code>True</code></p></li>
</ul>

<p>For advanced uses, you can turn your project into a Flask Blueprint in order to
register template filters or dynamically set the template context.</p>

<pre><code class="python">from flask import Blueprint
blueprint = Blueprint('awesome_project', __name__)

# Register template filter
@blueprint.app_template_filter('my_filter')
def my_filter(text):
   return text.strip()

@blueprint.app_context_processor
def context_processor():
    """
    Add "my_variable" to context
    """
    context = {
        'my_variable': 'My variable would be more awesome in real life, like reading a file or API data.",
    }

    return context
</code></pre>

Now you can reference `{{ my_variable }}` in your templates, or call your filter on a template variable `{{ my_variable|my_filter }}`. 

## Base project

If any project contains a <code>URL_ROOT = ''</code> configuration, that project will:

* Be available at the root URL (`/index.html`, `/css/style.css`, etc).
* Always be published when deploying.

## JSON publishing

By default, every project's Google spreadsheet will be baked out to a JSON file representing each worksheet. For example, most projects will have a `myproject/json/values.json` that represents the contents of the "values" worksheet.

This means you can build pure Javascript apps using Tarbell in the framework of your choice. Just AJAX load or bootstrapping the JSON data.

To disable this behavior, add a line to your <code>config.py</code>

<pre><code class="python">CREATE_JSON = False</code></pre>

If you disable this behavior and need data available to Javascript applications, simply bootstrap the dataset provided it isn't too big. Here's something you might put in `myproject/index.html`:

<pre><code class="django">&#123;% block scripts %&#125;
&lt;script type="text/javascript"&gt;
    // Convert whole worksheet to JSON
    var authors = &#123;&#123 authors|tojson &#125;&#125;

    // Filter a worksheet
    var locations = [ &#123;% for address in locations %&#125;
        { state: '&#123;&#123 address.state &#125;&#125;' },
    &#123;% endfor %&#125; ];

    // Now process or display 'authors' and 'locations' ...
&lt;/script&gt;
&#123;% endblock %&#125;</code></pre>
